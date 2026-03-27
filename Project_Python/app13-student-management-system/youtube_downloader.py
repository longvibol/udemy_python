import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLineEdit, QPushButton, QLabel, QMessageBox, QProgressBar)
from PyQt6.QtCore import QThread, pyqtSignal, Qt

# Try to import yt_dlp, handle if missing
try:
    import yt_dlp
except ImportError:
    yt_dlp = None

class DownloadWorker(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        if yt_dlp is None:
            self.error.emit("yt-dlp library is missing. Please install it using: pip install yt-dlp")
            return

        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': '%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
                'noplaylist': True,  # Download only the video, not the whole playlist
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.status.emit("Fetching video info...")
                # Extract info first to get the title
                info = ydl.extract_info(self.url, download=False)
                video_title = info.get('title', 'Video')
                
                self.status.emit(f"Downloading: {video_title}")
                ydl.download([self.url])
            
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    percentage = int((downloaded / total) * 100)
                    self.progress.emit(percentage)
            except:
                pass
        elif d['status'] == 'finished':
            self.progress.emit(100)
            self.status.emit("Processing...")

class YoutubeDownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional YouTube Downloader")
        self.setFixedWidth(500)
        self.setFixedHeight(250)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Title Label
        title_label = QLabel("YouTube Video Downloader")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)

        # URL Input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL here...")
        layout.addWidget(self.url_input)

        # Download Button
        self.download_btn = QPushButton("Download Video")
        self.download_btn.clicked.connect(self.start_download)
        layout.addWidget(self.download_btn)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Status Label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

    def start_download(self):
        url = self.url_input.text()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a URL")
            return

        self.download_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        
        self.worker = DownloadWorker(url)
        self.worker.status.connect(self.update_status)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.download_finished)
        self.worker.error.connect(self.download_error)
        self.worker.start()

    def update_status(self, message):
        self.status_label.setText(message)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def download_finished(self):
        self.status_label.setText("Download Completed!")
        self.progress_bar.setValue(100)
        self.download_btn.setEnabled(True)
        QMessageBox.information(self, "Success", "Video downloaded successfully!")

    def download_error(self, message):
        self.status_label.setText("Error occurred")
        self.download_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", f"An error occurred: {message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YoutubeDownloaderApp()
    window.show()
    sys.exit(app.exec())
