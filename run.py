from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    # Run the app with SocketIO support
    socketio.run(app, 
                host='0.0.0.0',
                port=5000, 
                debug=True,
                use_reloader=True,
                allow_unsafe_werkzeug=True)  # Only for development