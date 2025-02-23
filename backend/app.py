import os
import uuid
import subprocess
import shutil
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)
app.config['STATIC_DIR'] = os.path.join(os.path.dirname(__file__), 'static')
app.config['MEDIA_DIR'] = os.path.join(os.path.dirname(__file__), 'media')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Ensure directories exist
os.makedirs(app.config['STATIC_DIR'], exist_ok=True)
os.makedirs(app.config['MEDIA_DIR'], exist_ok=True)

@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/render', methods=['POST'])
def render_animation():
    data = request.get_json()
    if not data or 'script' not in data:
        return jsonify({'error': 'No script provided'}), 400
    
    script = data['script']
    render_id = str(uuid.uuid4())
    
    # File paths
    temp_script = os.path.join(app.config['MEDIA_DIR'], f'temp_{render_id}.py')
    output_dir = os.path.join(app.config['MEDIA_DIR'], 'videos')
    final_output = os.path.join(app.config['STATIC_DIR'], f'output_{render_id}.mp4')
    
    try:
        # Save temporary script
        with open(temp_script, 'w') as f:
            f.write(script)
        
        # Run Manim render command
        cmd = [
            'manim',
            '-ql',  # Low quality for faster rendering
            '--progress_bar', 'none',
            '--media_dir', app.config['MEDIA_DIR'],
            temp_script,
            'MainScene'  # Assuming the script contains a MainScene class
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30  # Adjust timeout as needed
        )
        
        if result.returncode != 0:
            return jsonify({
                'error': 'Render failed',
                'details': result.stderr
            }), 500

        # Find generated video file
        video_path = os.path.join(
            output_dir,
            f'temp_{render_id}',
            '480p15',
            'MainScene.mp4'
        )
        
        if not os.path.exists(video_path):
            return jsonify({'error': 'Output video not found'}), 500
        
        # Move to static directory
        os.makedirs(os.path.dirname(final_output), exist_ok=True)
        shutil.move(video_path, final_output)
        
        return jsonify({
            'video_url': f'/static/output_{render_id}.mp4'
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Render timed out'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Cleanup temporary files
        if os.path.exists(temp_script):
            os.remove(temp_script)
        temp_dir = os.path.join(output_dir, f'temp_{render_id}')
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['STATIC_DIR'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
