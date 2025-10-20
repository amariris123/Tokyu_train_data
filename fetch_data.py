import requests
import json
from datetime import datetime

API_GATEWAY_URL = "https://04x5f9ykzc.execute-api.ap-northeast-1.amazonaws.com/prod/external-data-url?key=toyoko.json"

OUTPUT_FILENAME = "toyoko_data.json"

def get_signed_url(api_url):
    """API Gatewayから署名付きURLを取得する。"""
    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 署名付きURLを取得中...")
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('url')
    except Exception as e:
        print(f"エラー: 署名付きURLの取得に失敗しました: {e}")
        return None

def fetch_and_save_json(target_url, filename):
    """ターゲットURLからJSONデータを取得し、ファイルに保存する。"""
    print("S3から運行JSONデータを取得中...")
    try:
        response = requests.get(target_url, allow_redirects=True, timeout=10)
        response.raise_for_status()
        
        fetched_data = response.json()
        
        # publicディレクトリに出力することで、Vercel/Netlifyで公開対象になります
        # ディレクトリがない場合は事前に作成が必要です
        output_path = f"public/{filename}" 
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # 読みやすいようにインデントを付けて保存
            json.dump(fetched_data, f, ensure_ascii=False, indent=4)
        
        print(f"成功: JSONデータを {output_path} に保存しました。")
        return True

    except Exception as e:
        print(f"エラー: JSONデータの取得・保存に失敗しました: {e}")
        return False

def main():
    signed_url = get_signed_url(API_GATEWAY_URL)
    
    if signed_url:
        fetch_and_save_json(signed_url, OUTPUT_FILENAME)
    else:
        print("処理を中断します。")

if __name__ == "__main__":
    main()
