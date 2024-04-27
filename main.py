from bottle import Bottle, request, response, static_file
import os
import magic

app = Bottle()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# ファイルをアップロードするエンドポイント
@app.post('/upload')
def upload_file():
    upload_folder = 'uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    upload_file = request.files.get('file')
    if upload_file:
        # ファイルサイズのチェック
        if upload_file.content_length > MAX_FILE_SIZE:
            response.status = 400
            return {'status': 'error', 'message': 'File size exceeds the limit.'}

        # ファイルのマジックナンバーを取得
        file_magic = magic.Magic(mime=True)
        mime_type = file_magic.from_buffer(upload_file.file.read(1024))

        # ファイルのMIMEタイプから拡張子を取得
        ext = mime_type.split('/')[1]

        # 拡張子のチェック
        if ext not in ALLOWED_EXTENSIONS:
            response.status = 400
            return {'status': 'error', 'message': 'File type not allowed.'}

        # アップロードされたファイルのファイル名を取得
        filename = upload_file.raw_filename

        # ファイルを保存
        file_path = os.path.join(upload_folder, filename)
        upload_file.file.seek(0)  # ファイルポインタを先頭に戻す
        upload_file.save(file_path)
        return {'status': 'success', 'message': 'File uploaded successfully.', 'file_path': file_path}
    else:
        response.status = 400
        return {'status': 'error', 'message': 'No file uploaded.'}

# ファイルをダウンロードするエンドポイント
@app.get('/download/<filename>')
def download_file(filename):
    file_path = os.path.join('uploads', filename)
    if os.path.exists(file_path):
        return static_file(filename, root='uploads', download=filename)
    else:
        response.status = 404
        return {'status': 'error', 'message': 'File not found.'}

# ファイル一覧を取得するエンドポイント
@app.get('/list-files')
def list_files():
    upload_folder = 'uploads'
    files = []
    for filename in os.listdir(upload_folder):
        if os.path.isfile(os.path.join(upload_folder, filename)):
            files.append(filename)
    return {'files': files}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

