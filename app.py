from app import create_app, init_db

app = create_app()

if __name__ == '__main__':
    # 如果資料庫檔案不存在，可以在這裡自動初始化（開發用）
    # init_db() 
    app.run(debug=True)
