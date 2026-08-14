from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['GET'])
def download():
    # GET মেথড দিয়ে সরাসরি কুয়েরি প্যারামিটার থেকে লিংক নেওয়া
    url = request.args.get('url')
    
    if not url:
        return jsonify({'success': False, 'message': 'দয়া করে একটি টিকটক লিংক দিন।'})

    try:
        # TikWM API কল
        api_url = f"https://www.tikwm.com/api/?url={url}"
        response = requests.get(api_url)
        res_data = response.json()

        if res_data.get('code') == 0:
            video_info = res_data.get('data', {})
            return jsonify({
                'success': True,
                'title': video_info.get('title'),
                'author': video_info.get('author', {}).get('nickname'),
                'avatar': video_info.get('author', {}).get('avatar'),
                'video': video_info.get('play'), # ওয়াটারমার্ক ছাড়া ভিডিও লিংক
                'music': video_info.get('music')  # অডিও লিংক
            })
        else:
            return jsonify({'success': False, 'message': 'ভিডিও পাওয়া যায়নি। সঠিক লিংক প্রদান করুন।'})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': 'সার্ভারে সমস্যা হয়েছে। পরে আবার চেষ্টা করুন।'})

if __name__ == '__main__':
    app.run(debug=True)