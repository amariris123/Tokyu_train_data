import requests
import json
from datetime import datetime
import os
import sys

API_GATEWAY_MAP = {
    'toyoko.json': "https://04x5f9ykzc.execute-api.ap-northeast-1.amazonaws.com/prod/external-data-url",
    'meguro.json': "https://04x5f9ykzc.execute-api.ap-northeast-1.amazonaws.com/prod/external-data-url",
    'shinyokohama.json': "https://04x5f9ykzc.execute-api.ap-northeast-1.amazonaws.com/prod/external-data-url",
    'dento.json': "https://fp5owad3w3.execute-api.ap-northeast-1.amazonaws.com/prod/external-data-url",
    'oimachi.json': "https://fp5owad3w3.execute-api.ap-northeast-1.amazonaws.com/prod/external-data-url"
}

def get_signed_url(line_key):
    base_url = API_GATEWAY_MAP.get(line_key)
    if not base_url:
        print(f"エラー: 未知の路線キーです: {line_key}")
        return None
        
    api_url = f"{base_url}?key={line_key}"
    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {line_key} の運行情報を取得中･･･⏱")
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('url')
    except Exception as e:
        print(f"エラー: {line_key} の情報取得に失敗しました: {e}")
        return None

def fetch_and_save_json(target_url, output_path):
    print(f"運行情報データを取得中 -> {output_path}...")
    try:
        response = requests.get(target_url, allow_redirects=True, timeout=10)
        response.raise_for_status()
        
        fetched_data = response.json()
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
        
            json.dump(fetched_data, f, ensure_ascii=False, indent=4)
            
        print(f"成功: JSONデータを {output_path} に保存しました。")
        return True

    except Exception as e:
        print(f"エラー: JSONデータの取得・保存に失敗しました: {e}")
        return False

def process_line(line_key):
    output_filename = line_key
    output_path = f"public/{output_filename}"
    
    signed_url = get_signed_url(line_key)
    
    if signed_url:
        fetch_and_save_json(signed_url, output_path)
    else:
        print(f"{line_key} の処理を中断します。")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python fetch_data.py <路線キー e.g., toyoko.json>")
        sys.exit(1)
        
    LINE_KEY = sys.argv[1]
    process_line(LINE_KEY)
