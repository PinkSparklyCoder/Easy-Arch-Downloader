import requests
import sys
import os
import json
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tqdm import tqdm
import time
import hashlib
import argparse
import shutil
import math
import webbrowser
import logging

# -----------------------
# Logging + Config files
# -----------------------
# Log to file for improved error reporting/debugging
LOG_FILE = "arch_downloader.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
)

# Persisted settings file
CONFIG_FILE = "arch_downloader_config.json"
# history functionality removed

# -----------------------
# Translations
# -----------------------
# Added Korean (ko), Mandarin simplified (zh), Afrikaans (af), German (de), French (fr)
LANGUAGES = {
    "en": {
        "detecting_country": "Detecting your country...",
        "detected_country": "Detected country: {}",
        "fetching_mirrors": "Fetching mirrors...",
        "no_mirrors": "No mirrors found for your country.",
        "available_mirrors": "Available mirrors:",
        "select_mirror": "Select a mirror:",
        "mirror_speed": "Testing mirror speed...",
        "downloading": "Downloading {} ...",
        "download_complete": "Downloaded to {}",
        "checksum_verifying": "Verifying checksum...",
        "checksum_ok": "Checksum OK!",
        "checksum_fail": "Checksum failed!",
        "choose_location": "Choose save location",
        "download_failed": "Download failed, retrying...",
        "download_history": "Download history:",
        "exit": "Exit",
        "start_download": "Start Download",
        "language": "Language",
        "mirror_speed_label": "Speed: {:.2f} MB/s",
        "iso_not_found": "Could not find ISO on the selected mirror.",
        "invalid_choice": "Invalid choice.",
        "history_saved": "History saved.",
        "select_iso": "Select ISO to verify",
        "checksum_verified": "Checksum verified.",
        "checksum_not_found": "Checksum file not found.",
        "mirror_testing": "Testing mirrors...",
        "mirror_tested": "Tested {} mirrors.",
        "gui_title": "Arch Linux ISO Downloader",
        "gui_download": "Download",
        "gui_verify": "Verify (optional)",
        "gui_history": "Show History",
        "gui_choose": "Choose...",
        "gui_quit": "Quit",
        "open_folder": "Open folder",
        "cancel": "Cancel",
        "pause": "Pause",
        "resume": "Resume",
        "insufficient_space": "Insufficient disk space: need ~{:.2f} GB, have {:.2f} GB",
        "show_help": "Help / Create bootable USB",
        "help_text": "Links and short instructions:\n- Rufus (Windows): https://rufus.ie\n- balenaEtcher: https://www.balena.io/etcher/\n- dd (Linux/macOS): sudo dd if=arch.iso of=/dev/sdX bs=4M status=progress",
        "settings_saved": "Settings saved.",
        "resume_supported": "Resume supported (server accepts Range).",
        "resume_not_supported": "Resume not supported by server; full re-download will occur.",
        "eta_label": "Speed: {speed:.2f} MB/s  ETA: {eta}",
    },
    "es": {
        "detecting_country": "Detectando tu país...",
        "detected_country": "País detectado: {}",
        "fetching_mirrors": "Obteniendo espejos...",
        "no_mirrors": "No se encontraron espejos para tu país.",
        "available_mirrors": "Espejos disponibles:",
        "select_mirror": "Selecciona un espejo:",
        "mirror_speed": "Probando velocidad del espejo...",
        "downloading": "Descargando {} ...",
        "download_complete": "Descargado en {}",
        "checksum_verifying": "Verificando suma de verificación...",
        "checksum_ok": "¡Suma de verificación OK!",
        "checksum_fail": "¡Suma de verificación fallida!",
        "choose_location": "Elige ubicación para guardar",
        "download_failed": "Descarga fallida, reintentando...",
        "download_history": "Historial de descargas:",
        "exit": "Salir",
        "start_download": "Iniciar descarga",
        "language": "Idioma",
        "mirror_speed_label": "Velocidad: {:.2f} MB/s",
        "iso_not_found": "No se pudo encontrar el ISO en el espejo seleccionado.",
        "invalid_choice": "Opción inválida.",
        "history_saved": "Historial guardado.",
        "select_iso": "Selecciona ISO para verificar",
        "checksum_verified": "Suma de verificación verificada.",
        "checksum_not_found": "Archivo de suma de verificación no encontrado.",
        "mirror_testing": "Probando espejos...",
        "mirror_tested": "Probados {} espejos.",
        "gui_title": "Descargador de ISO de Arch Linux",
        "gui_download": "Descargar",
        "gui_verify": "Verificar (opcional)",
        "gui_history": "Mostrar historial",
        "gui_choose": "Elegir...",
        "gui_quit": "Salir",
        "open_folder": "Abrir carpeta",
        "cancel": "Cancelar",
        "pause": "Pausar",
        "resume": "Reanudar",
        "insufficient_space": "Espacio insuficiente: se necesitan ~{:.2f} GB, hay {:.2f} GB",
        "show_help": "Ayuda / Crear USB booteable",
        "help_text": "Enlaces y breves instrucciones:\n- Rufus (Windows): https://rufus.ie\n- balenaEtcher: https://www.balena.io/etcher/\n- dd (Linux/macOS): sudo dd if=arch.iso of=/dev/sdX bs=4M status=progress",
        "settings_saved": "Configuración guardada.",
        "resume_supported": "Reanudar soportado (el servidor acepta Range).",
        "resume_not_supported": "Reanudar no soportado por el servidor; se descargará completo.",
        "eta_label": "Velocidad: {speed:.2f} MB/s  ETA: {eta}",
    },
    "ko": {  # Korean
        "detecting_country": "국가를 감지하는 중...",
        "detected_country": "감지된 국가: {}",
        "fetching_mirrors": "미러 가져오는 중...",
        "no_mirrors": "해당 국가의 미러가 없습니다.",
        "available_mirrors": "사용 가능한 미러:",
        "select_mirror": "미러를 선택하세요:",
        "mirror_speed": "미러 속도 테스트 중...",
        "downloading": "{} 다운로드 중 ...",
        "download_complete": "{}에 다운로드 완료",
        "checksum_verifying": "체크섬 확인 중...",
        "checksum_ok": "체크섬 정상!",
        "checksum_fail": "체크섬 불일치!",
        "choose_location": "저장 위치 선택",
        "download_failed": "다운로드 실패, 재시도 중...",
        "download_history": "다운로드 기록:",
        "exit": "종료",
        "start_download": "다운로드 시작",
        "language": "언어",
        "mirror_speed_label": "속도: {:.2f} MB/s",
        "iso_not_found": "선택한 미러에서 ISO를 찾을 수 없습니다.",
        "invalid_choice": "잘못된 선택입니다.",
        "history_saved": "기록 저장됨.",
        "select_iso": "검증할 ISO 선택",
        "checksum_verified": "체크섬 검증 완료.",
        "checksum_not_found": "체크섬 파일을 찾을 수 없습니다.",
        "mirror_testing": "미러 테스트 중...",
        "mirror_tested": "{}개의 미러 테스트 완료.",
        "gui_title": "Arch Linux ISO 다운로더",
        "gui_download": "다운로드",
        "gui_verify": "검증 (선택)",
        "gui_history": "기록 보기",
        "gui_choose": "선택...",
        "gui_quit": "종료",
        "open_folder": "폴더 열기",
        "cancel": "취소",
        "pause": "일시정지",
        "resume": "다시시작",
        "insufficient_space": "디스크 공간 부족: 필요 약 {:.2f} GB, 사용 가능 {:.2f} GB",
        "show_help": "도움말 / 부팅 USB 만들기",
        "help_text": "링크 및 간단한 지침:\n- Rufus (Windows): https://rufus.ie\n- balenaEtcher: https://www.balena.io/etcher/\n- dd (Linux/macOS): sudo dd if=arch.iso of=/dev/sdX bs=4M status=progress",
        "settings_saved": "설정 저장됨.",
        "resume_supported": "재개 가능 (서버가 Range를 허용함).",
        "resume_not_supported": "서버가 재개를 지원하지 않음; 전체 재다운로드가 발생합니다.",
        "eta_label": "속도: {speed:.2f} MB/s  ETA: {eta}",
    },
    "zh": {  # Mandarin (simplified)
        "detecting_country": "正在检测国家...",
        "detected_country": "检测到国家：{}",
        "fetching_mirrors": "正在获取镜像...",
        "no_mirrors": "未找到您国家的镜像。",
        "available_mirrors": "可用镜像：",
        "select_mirror": "选择镜像：",
        "mirror_speed": "测试镜像速度...",
        "downloading": "正在下载 {} ...",
        "download_complete": "下载到 {}",
        "checksum_verifying": "正在验证校验和...",
        "checksum_ok": "校验通过！",
        "checksum_fail": "校验失败！",
        "choose_location": "选择保存位置",
        "download_failed": "下载失败，重试中...",
        "download_history": "下载历史：",
        "exit": "退出",
        "start_download": "开始下载",
        "language": "语言",
        "mirror_speed_label": "速度：{:.2f} MB/s",
        "iso_not_found": "在所选镜像上找不到 ISO。",
        "invalid_choice": "无效选择。",
        "history_saved": "历史已保存。",
        "select_iso": "选择要验证的 ISO",
        "checksum_verified": "校验已验证。",
        "checksum_not_found": "未找到校验文件。",
        "mirror_testing": "正在测试镜像...",
        "mirror_tested": "测试了 {} 个镜像。",
        "gui_title": "Arch Linux ISO 下载器",
        "gui_download": "下载",
        "gui_verify": "验证 (可选)",
        "gui_history": "显示历史",
        "gui_choose": "选择...",
        "gui_quit": "退出",
        "open_folder": "打开文件夹",
        "cancel": "取消",
        "pause": "暂停",
        "resume": "继续",
        "insufficient_space": "磁盘空间不足：需要约 {:.2f} GB，剩余 {:.2f} GB",
        "show_help": "帮助 / 制作可引导 USB",
        "help_text": "链接与简要说明：\n- Rufus (Windows): https://rufus.ie\n- balenaEtcher: https://www.balena.io/etcher/\n- dd (Linux/macOS): sudo dd if=arch.iso of=/dev/sdX bs=4M status=progress",
        "settings_saved": "设置已保存。",
        "resume_supported": "支持续传（服务器接受 Range）。",
        "resume_not_supported": "服务器不支持续传；将进行完整重下载。",
        "eta_label": "速度：{speed:.2f} MB/s  预计剩余：{eta}",
    },
    "af": {  # Afrikaans
        "detecting_country": "Besig om jou land te vind...",
        "detected_country": "Gevonde land: {}",
        "fetching_mirrors": "Haal spieëls op...",
        "no_mirrors": "Geen spieëls gevind vir jou land nie.",
        "available_mirrors": "Beskikbare spieëls:",
        "select_mirror": "Kies 'n spieël:",
        "mirror_speed": "Toets spieël spoed...",
        "downloading": "Laai af {} ...",
        "download_complete": "Aflaai voltooi na {}",
        "checksum_verifying": "Kontroleer checksum...",
        "checksum_ok": "Checksum OK!",
        "checksum_fail": "Checksum het misluk!",
        "choose_location": "Kies stoorplek",
        "download_failed": "Aflaai het misluk, probeer weer...",
        "download_history": "Aflaaigeskiedenis:",
        "exit": "Verlaat",
        "start_download": "Begin aflaai",
        "language": "Taal",
        "mirror_speed_label": "Spoed: {:.2f} MB/s",
        "iso_not_found": "Kon ISO nie op die gekose spieël vind nie.",
        "invalid_choice": "Ongeldige keuse.",
        "history_saved": "Geskiedenis gestoor.",
        "select_iso": "Kies ISO om te verifieer",
        "checksum_verified": "Checksum geverifieer.",
        "checksum_not_found": "Kontrolesom-lêer nie gevind nie.",
        "mirror_testing": "Toets spieëls...",
        "mirror_tested": "Getoets {} spieëls.",
        "gui_title": "Arch Linux ISO Aflaaier",
        "gui_download": "Laai af",
        "gui_verify": "Verifieer (opsioneel)",
        "gui_history": "Wys geskiedenis",
        "gui_choose": "Kies...",
        "gui_quit": "Terug",
        "open_folder": "Maak gids oop",
        "cancel": "Kanselleer",
        "pause": "Pouse",
        "resume": "Hervat",
        "insufficient_space": "Onvoldoende skyfspasie: benodig ~{:.2f} GB, het {:.2f} GB",
        "show_help": "Hulp / Skep bootbare USB",
        "help_text": "Skakels en kort instruksies:\n- Rufus (Windows): https://rufus.ie\n- balenaEtcher: https://www.balena.io/etcher/\n- dd (Linux/macOS): sudo dd if=arch.iso of=/dev/sdX bs=4M status=progress",
        "settings_saved": "Instellings gestoor.",
        "resume_supported": "Hervat ondersteun (bediener aanvaar Range).",
        "resume_not_supported": "Hervat nie ondersteun nie; volle her-aflaai sal plaasvind.",
        "eta_label": "Spoed: {speed:.2f} MB/s  ETA: {eta}",
    },
    "de": {  # German
        "detecting_country": "Ermittle Ihr Land...",
        "detected_country": "Erkanntes Land: {}",
        "fetching_mirrors": "Hole Mirror-Liste...",
        "no_mirrors": "Keine Mirrors für Ihr Land gefunden.",
        "available_mirrors": "Verfügbare Mirrors:",
        "select_mirror": "Wählen Sie einen Mirror:",
        "mirror_speed": "Teste Mirror-Geschwindigkeit...",
        "downloading": "Lade {} herunter ...",
        "download_complete": "Heruntergeladen nach {}",
        "checksum_verifying": "Prüfe Prüfsumme...",
        "checksum_ok": "Prüfsumme OK!",
        "checksum_fail": "Prüfsumme fehlerhaft!",
        "choose_location": "Speicherort wählen",
        "download_failed": "Download fehlgeschlagen, versuche erneut...",
        "download_history": "Download-Verlauf:",
        "exit": "Beenden",
        "start_download": "Download starten",
        "language": "Sprache",
        "mirror_speed_label": "Geschw.: {:.2f} MB/s",
        "iso_not_found": "ISO auf ausgewähltem Mirror nicht gefunden.",
        "invalid_choice": "Ungültige Auswahl.",
        "history_saved": "Verlauf gespeichert.",
        "select_iso": "ISO zum Überprüfen auswählen",
        "checksum_verified": "Prüfsumme verifiziert.",
        "checksum_not_found": "Prüfsummendatei nicht gefunden.",
        "mirror_testing": "Teste Mirrors...",
        "mirror_tested": "{} Mirrors getestet.",
        "gui_title": "Arch Linux ISO Downloader",
        "gui_download": "Herunterladen",
        "gui_verify": "Überprüfen (optional)",
        "gui_history": "Verlauf anzeigen",
        "gui_choose": "Wählen...",
        "gui_quit": "Beenden",
        "open_folder": "Ordner öffnen",
        "cancel": "Abbrechen",
        "pause": "Pause",
        "resume": "Fortsetzen",
        "insufficient_space": "Nicht genug Speicherplatz: benötigt ~{:.2f} GB, vorhanden {:.2f} GB",
        "show_help": "Hilfe / Bootfähiges USB erstellen",
        "help_text": "Links und kurze Anleitung:\n- Rufus (Windows): https://rufus.ie\n- balenaEtcher: https://www.balena.io/etcher/\n- dd (Linux/macOS): sudo dd if=arch.iso of=/dev/sdX bs=4M status=progress",
        "settings_saved": "Einstellungen gespeichert.",
        "resume_supported": "Fortsetzen unterstützt (Server erlaubt Range).",
        "resume_not_supported": "Fortsetzen nicht unterstützt; vollständiger Neu-Download erfolgt.",
        "eta_label": "Geschw.: {speed:.2f} MB/s  ETA: {eta}",
    },
    "fr": {  # French
        "detecting_country": "Détection du pays...",
        "detected_country": "Pays détecté : {}",
        "fetching_mirrors": "Récupération des miroirs...",
        "no_mirrors": "Aucun miroir trouvé pour votre pays.",
        "available_mirrors": "Miroirs disponibles :",
        "select_mirror": "Sélectionnez un miroir :",
        "mirror_speed": "Test de vitesse des miroirs...",
        "downloading": "Téléchargement de {} ...",
        "download_complete": "Téléchargé vers {}",
        "checksum_verifying": "Vérification du checksum...",
        "checksum_ok": "Checksum OK !",
        "checksum_fail": "Checksum incorrect !",
        "choose_location": "Choisir l'emplacement",
        "download_failed": "Échec du téléchargement, réessai...",
        "download_history": "Historique des téléchargements :",
        "exit": "Quitter",
        "start_download": "Démarrer le téléchargement",
        "language": "Langue",
        "mirror_speed_label": "Vitesse : {:.2f} MB/s",
        "iso_not_found": "Impossible de trouver l'ISO sur le miroir sélectionné.",
        "invalid_choice": "Choix invalide.",
        "history_saved": "Historique enregistré.",
        "select_iso": "Sélectionnez l'ISO à vérifier",
        "checksum_verified": "Checksum vérifié.",
        "checksum_not_found": "Fichier checksum introuvable.",
        "mirror_testing": "Test des miroirs...",
        "mirror_tested": "{} miroirs testés.",
        "gui_title": "Téléchargeur ISO Arch Linux",
        "gui_download": "Télécharger",
        "gui_verify": "Vérifier (optionnel)",
        "gui_history": "Afficher l'historique",
        "gui_choose": "Choisir...",
        "gui_quit": "Quitter",
        "open_folder": "Ouvrir le dossier",
        "cancel": "Annuler",
        "pause": "Pause",
        "resume": "Reprendre",
        "insufficient_space": "Espace disque insuffisant : besoin d'environ {:.2f} GB, disponible {:.2f} GB",
        "show_help": "Aide / Créer une clé USB bootable",
        "help_text": "Liens et instructions courtes :\n- Rufus (Windows): https://rufus.ie\n- balenaEtcher: https://www.balena.io/etcher/\n- dd (Linux/macOS): sudo dd if=arch.iso of=/dev/sdX bs=4M status=progress",
        "settings_saved": "Paramètres enregistrés.",
        "resume_supported": "Reprise prise en charge (le serveur accepte Range).",
        "resume_not_supported": "Reprise non prise en charge ; un nouveau téléchargement complet aura lieu.",
        "eta_label": "Vitesse : {speed:.2f} MB/s  ETA : {eta}",
    },
    "ja": {  # Japanese
        "detecting_country": "国を検出しています...",
        "detected_country": "検出された国: {}",
        "fetching_mirrors": "ミラーを取得しています...",
        "no_mirrors": "お住まいの国のミラーが見つかりません。",
        "available_mirrors": "利用可能なミラー:",
        "select_mirror": "ミラーを選択してください:",
        "mirror_speed": "ミラースピードをテストしています...",
        "downloading": "{} をダウンロード中 ...",
        "download_complete": "{} にダウンロードしました",
        "checksum_verifying": "チェックサムを検証しています...",
        "checksum_ok": "チェックサム OK!",
        "checksum_fail": "チェックサムが一致しません！",
        "choose_location": "保存先を選択",
        "download_failed": "ダウンロードに失敗しました。再試行中...",
        "download_history": "ダウンロード履歴:",
        "exit": "終了",
        "start_download": "ダウンロード開始",
        "language": "言語",
        "mirror_speed_label": "速度: {:.2f} MB/s",
        "iso_not_found": "選択したミラーに ISO が見つかりません。",
        "invalid_choice": "無効な選択です。",
        "history_saved": "履歴を保存しました。",
        "select_iso": "検証する ISO を選択",
        "checksum_verified": "チェックサムが検証されました。",
        "checksum_not_found": "チェックサムファイルが見つかりません。",
        "mirror_testing": "ミラーをテストしています...",
        "mirror_tested": "{} 個のミラーをテストしました。",
        "gui_title": "Arch Linux ISO ダウンローダー",
        "gui_download": "ダウンロード",
        "gui_verify": "検証 (オプション)",
        "gui_history": "履歴を表示",
        "gui_choose": "選択...",
        "gui_quit": "終了",
        "open_folder": "フォルダーを開く",
        "cancel": "キャンセル",
        "pause": "一時停止",
        "resume": "再開",
        "insufficient_space": "ディスク容量が不足しています: 約 {:.2f} GB が必要、使用可能 {:.2f} GB",
        "show_help": "ヘルプ / ブータブルUSB作成",
        "help_text": "リンクと簡単な手順:\n- Rufus (Windows): https://rufus.ie\n- balenaEtcher: https://www.balena.io/etcher/\n- dd (Linux/macOS): sudo dd if=arch.iso of=/dev/sdX bs=4M status=progress",
        "settings_saved": "設定を保存しました。",
        "resume_supported": "再開がサポートされています (サーバーが Range を受け入れます)。",
        "resume_not_supported": "サーバーが再開をサポートしていません; フル再ダウンロードが発生します。",
        "eta_label": "速度: {speed:.2f} MB/s  残り: {eta}",
    },
}

def _(key, lang="en"):
    """Return translated string for key and language; fallback to English or key."""
    return LANGUAGES.get(lang, LANGUAGES["en"]).get(key, LANGUAGES["en"].get(key, key))

# -----------------------
# Utility functions
# -----------------------
def load_config():
    """Load persisted configuration (last folder, language, verify option)."""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logging.exception("Failed loading config")
    return {"last_folder": os.path.expanduser("~"), "lang": "en", "verify": True, "window": None}

def save_config(cfg):
    """Save configuration to disk."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        logging.info("Settings saved")
    except Exception:
        logging.exception("Failed saving config")

def get_country():
    """Detect country using external IP geolocation (ipinfo.io)."""
    try:
        resp = requests.get("https://ipinfo.io/json", timeout=5)
        resp.raise_for_status()
        return resp.json().get("country")
    except Exception:
        logging.exception("get_country failed")
        return None

def get_mirrors(country):
    """Fetch mirror list from archlinux.org and filter by country and active status."""
    url = "https://archlinux.org/mirrors/status/json/"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        mirrors = resp.json().get("urls", [])
        return [m for m in mirrors if m.get("country_code") == country and m.get("active")]
    except Exception:
        logging.exception("get_mirrors failed")
        return []

def test_mirror_speed(mirror_url, timeout=5):
    """
    Quick responsiveness + throughput estimation:
    - Request the /iso/latest/ page and read a small chunk to estimate responsiveness.
    - Returns estimated MB/s (may be coarse but useful for ranking).
    """
    test_url = mirror_url.rstrip("/") + "/iso/latest/"
    try:
        start = time.time()
        resp = requests.get(test_url, stream=True, timeout=timeout)
        resp.raise_for_status()
        chunk = resp.raw.read(16384)  # read up to 16 KB
        elapsed = time.time() - start
        size = len(chunk) or 10240
        speed = (size / (1024 * 1024)) / (elapsed if elapsed > 0 else 1)
        return speed
    except Exception:
        return 0.0

def get_latest_iso_url(mirror_url):
    """
    Parse /iso/latest/ HTML and return first .iso link found.
    Returns absolute URL when possible.
    """
    iso_page = mirror_url.rstrip("/") + "/iso/latest/"
    try:
        resp = requests.get(iso_page, timeout=10)
        resp.raise_for_status()
        for line in resp.text.splitlines():
            if ".iso" in line and "href" in line:
                start = line.find("href=\"")
                if start >= 0:
                    start += 6
                    end = line.find(".iso", start)
                    if end >= 0:
                        end += 4
                        href = line[start:end]
                        if href.startswith("http"):
                            return href
                        return iso_page + href.lstrip("/")
    except Exception:
        logging.exception("get_latest_iso_url failed for %s", mirror_url)
    return None

def get_checksum_url(mirror_url, iso_filename):
    """Construct checksum (.sha256) URL for iso in mirror's iso/latest/ folder."""
    iso_page = mirror_url.rstrip("/") + "/iso/latest/"
    checksum_file = iso_filename + ".sha256"
    return iso_page + checksum_file

# -----------------------
# Download with resume + progress + cancel
# -----------------------
def download_iso(iso_url, filename, lang="en", retries=3, progress_callback=None, stop_event=None):
    """
    Download ISO with support for:
    - resuming via HTTP Range if server supports it
    - reporting progress via progress_callback(downloaded_bytes, total_bytes, speed_bytes_per_sec)
    - cancellation via stop_event (threading.Event)
    Returns True on success, False on failure or cancelled.
    """
    headers = {}
    # if file exists, attempt resume
    try:
        existing = os.path.getsize(filename) if os.path.exists(filename) else 0
    except Exception:
        existing = 0

    for attempt in range(retries):
        try:
            # Use Range header to resume if file partially exists
            if existing > 0:
                headers["Range"] = f"bytes={existing}-"
            with requests.get(iso_url, stream=True, timeout=15, headers=headers) as r:
                r.raise_for_status()
                # determine total size
                total = 0
                content_range = r.headers.get("Content-Range")
                if content_range:
                    # Content-Range: bytes start-end/total
                    try:
                        total = int(content_range.split("/")[-1])
                    except Exception:
                        total = 0
                else:
                    total = int(r.headers.get("content-length", 0))
                    if existing:
                        # server didn't support Range; we'll re-download full file
                        existing = 0

                mode = "ab" if existing and (r.status_code == 206) else "wb"
                downloaded = existing
                start_time = time.time()
                last_time = start_time
                last_downloaded = downloaded

                # if callback provided, initialize
                if progress_callback:
                    try:
                        progress_callback(downloaded, total, 0.0)
                    except Exception:
                        pass

                with open(filename, mode) as f:
                    for chunk in r.iter_content(chunk_size=131072):
                        if stop_event and stop_event.is_set():
                            logging.info("Download cancelled by user")
                            return False
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            now = time.time()
                            elapsed = now - last_time
                            if elapsed >= 0.5:
                                speed = (downloaded - last_downloaded) / (now - last_time)
                                last_time = now
                                last_downloaded = downloaded
                                if progress_callback:
                                    try:
                                        progress_callback(downloaded, total, speed)
                                    except Exception:
                                        pass
                # final callback
                if progress_callback:
                    try:
                        progress_callback(downloaded, total, 0.0)
                    except Exception:
                        pass
            logging.info("Download completed: %s", filename)
            return True
        except Exception as e:
            logging.exception("download_iso attempt %d failed", attempt + 1)
            time.sleep(1)
    return False

# -----------------------
# Checksum (optional)
# -----------------------
# verify_checksum removed — checksum verification feature removed

# -----------------------
# History & misc utils
# -----------------------
# save_history removed — download history feature removed

def open_folder(path):
    """Open folder in OS file explorer (Windows: os.startfile)."""
    try:
        if os.path.isdir(path):
            os.startfile(path)
    except Exception:
        logging.exception("open_folder failed")

# -----------------------
# CLI entrypoint
# -----------------------
def main_cli(args):
    """Command-line mode: detect country, list mirrors, let user choose, download (with optional verify)."""
    cfg = load_config()
    lang = args.lang or cfg.get("lang", "en")
    print(_( "detecting_country", lang))
    country = get_country()
    if not country:
        print(_( "no_mirrors", lang))
        sys.exit(1)
    print(_( "detected_country", lang).format(country))

    print(_( "fetching_mirrors", lang))
    mirrors = get_mirrors(country)
    if not mirrors:
        print(_( "no_mirrors", lang))
        sys.exit(1)

    print(_( "mirror_testing", lang))
    spds = [test_mirror_speed(m["url"]) for m in mirrors]
    sorted_pairs = sorted(zip(spds, mirrors), key=lambda x: x[0], reverse=True)
    mirrors = [m for _, m in sorted_pairs]

    for i, m in enumerate(mirrors):
        print(f"{i+1}: {m['url']} ({m.get('protocol')}) - " + _( "mirror_speed_label", lang).format(spds[i] if i < len(spds) else 0.0))

    choice = input(_( "select_mirror", lang) + f" [1-{len(mirrors)}]: ")
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(mirrors):
            raise ValueError
        mirror_url = mirrors[idx]["url"]
    except Exception:
        print(_( "invalid_choice", lang))
        sys.exit(1)

    iso_url = get_latest_iso_url(mirror_url)
    if not iso_url:
        print(_( "iso_not_found", lang))
        sys.exit(1)

    filename = os.path.basename(iso_url)
    save_path = filedialog.asksaveasfilename(title=_( "choose_location", lang), initialfile=filename)
    if not save_path:
        print(_( "exit", lang))
        sys.exit(0)

    # quick disk space check
    try:
        stat = shutil.disk_usage(os.path.dirname(save_path) or ".")
        free_gb = stat.free / (1024 ** 3)
    except Exception:
        free_gb = 0
    # can't know exact total until headers are read, informally skip

    stop_event = threading.Event()

    def cb(downloaded, total, speed):
        # simple console progress
        if total:
            pct = downloaded / total * 100
            eta = "-"
            if speed > 0:
                eta_sec = (total - downloaded) / speed
                eta = f"{int(eta_sec)}s"
            print(f"\r{downloaded}/{total} bytes ({pct:.1f}%) speed={speed/1024/1024:.2f} MB/s ETA={eta}", end="")

    ok = download_iso(iso_url, save_path, lang, progress_callback=cb, stop_event=stop_event)
    print()
    if ok:
        # open folder button enabled
        print(_( "download_complete", lang).format(os.path.basename(save_path)))
    else:
        print(_( "download_failed", lang))

# -----------------------
# GUI entrypoint
# -----------------------
def main_gui():
    """
    GUI:
    - auto-detect country
    - fetch + rank mirrors (auto-select fastest)
    - allow folder selection
    - show progress bar with speed and ETA
    - cancel/pause (stop) and allow resume (relaunch download will resume via Range)
    - optional checksum verification toggle
    - show help panel with links
    - persist settings
    """
    cfg = load_config()
    root = tk.Tk()
    lang = cfg.get("lang", "en")
    root.title(_( "gui_title", lang))
    if cfg.get("window"):
        try:
            root.geometry(cfg["window"])
        except Exception:
            pass
    # Increased window size so all buttons are visible
    root.geometry("1000x620")
    root.resizable(True, True)

    # GUI state
    country_var = tk.StringVar(value="")
    iso_var = tk.StringVar()
    save_folder_var = tk.StringVar(value=cfg.get("last_folder", os.path.expanduser("~")))
    lang_var = tk.StringVar(value=cfg.get("lang", "en"))
    verify_var = tk.BooleanVar(value=cfg.get("verify", True))
    mirrors = []
    speeds = []
    download_thread = None
    stop_event = None
    downloading = threading.Event()

    # helper to update config when language/verify/last folder change
    def persist_settings():
        cfg["last_folder"] = save_folder_var.get()
        cfg["lang"] = lang_var.get()
        try:
            cfg["window"] = root.winfo_geometry()
        except Exception:
            pass
        save_config(cfg)
        messagebox.showinfo("", _( "settings_saved", lang_var.get()))

    def refresh_mirrors():
        """Fetch mirrors, test speeds, sort, populate listbox. Auto-select fastest mirror."""
        label_status.config(text=_( "fetching_mirrors", lang_var.get()))
        root.update()
        country = get_country()
        country_var.set(country or "")
        label_country.config(text=_( "detected_country", lang_var.get()).format(country or ""))
        ms = get_mirrors(country)
        label_status.config(text=_( "mirror_testing", lang_var.get()))
        root.update()
        spds = [test_mirror_speed(m["url"]) for m in ms]
        sorted_pairs = sorted(zip(spds, ms), key=lambda x: x[0], reverse=True)
        sorted_spds = [s for s, _ in sorted_pairs]
        sorted_ms = [m for _, m in sorted_pairs]
        nonlocal mirrors, speeds
        mirrors, speeds = sorted_ms, sorted_spds
        mirror_list.delete(0, tk.END)
        for i, m in enumerate(mirrors):
            mirror_list.insert(tk.END, f"{m['url']} ({m.get('protocol')}) - " + _( "mirror_speed_label", lang_var.get()).format(speeds[i] if i < len(speeds) else 0.0))
        if not mirrors:
            label_status.config(text=_( "no_mirrors", lang_var.get()))
            btn_download.config(state="disabled")
        else:
            label_status.config(text=_( "mirror_tested", lang_var.get()).format(len(mirrors)))
            btn_download.config(state="normal")
            # auto-select fastest
            mirror_list.select_clear(0, tk.END)
            mirror_list.select_set(0)
            mirror_list.see(0)

    def choose_folder():
        """Open directory chooser and store chosen folder."""
        folder = filedialog.askdirectory(title=_( "choose_location", lang_var.get()), initialdir=save_folder_var.get())
        if folder:
            save_folder_var.set(folder)

    def start_download():
        """Start download on selected mirror. Disable controls while downloading."""
        idx = mirror_list.curselection()
        if not idx or idx[0] < 0 or idx[0] >= len(mirrors):
            messagebox.showerror(_( "invalid_choice", lang_var.get()), _( "invalid_choice", lang_var.get()))
            return
        mirror_url = mirrors[idx[0]]["url"]
        iso_url = get_latest_iso_url(mirror_url)
        if not iso_url:
            messagebox.showerror(_( "iso_not_found", lang_var.get()), _( "iso_not_found", lang_var.get()))
            return
        filename = os.path.basename(iso_url)
        iso_var.set(filename)
        folder = save_folder_var.get()
        if not folder:
            choose_folder()
            folder = save_folder_var.get()
        if not folder:
            return
        save_path = os.path.join(folder, filename)

        # quick disk space check using content-length header
        try:
            # HEAD to check size
            resp = requests.head(iso_url, timeout=10)
            resp.raise_for_status()
            total = int(resp.headers.get("content-length", 0))
        except Exception:
            total = 0
        try:
            stat = shutil.disk_usage(folder)
            free_bytes = stat.free
        except Exception:
            free_bytes = 0
        if total and free_bytes and free_bytes < total:
            free_gb = free_bytes / (1024 ** 3)
            need_gb = total / (1024 ** 3)
            messagebox.showwarning("", _( "insufficient_space", lang_var.get()).format(need_gb, free_gb))

        # disable controls
        btn_download.config(state="disabled")
        btn_refresh.config(state="disabled")
        btn_choose_folder.config(state="disabled")
        mirror_list.config(state="disabled")
        lang_menu.config(state="disabled")
        verify_var.config(state="disabled")
        btn_cancel.config(state="normal")
        btn_pause.config(state="normal")
        downloading.set()
        persist_settings()

        nonlocal stop_event, download_thread
        stop_event = threading.Event()

        # progress stats for ETA
        stats = {"last_time": time.time(), "last_bytes": 0, "speed": 0.0}

        def progress_cb(downloaded, total, speed):
            """Update GUI progress bar, speed and ETA label (called from download thread)."""
            try:
                # compute speed and ETA nicely
                now = time.time()
                if speed and speed > 0:
                    speed_mb = speed / (1024 ** 2)
                    remaining = total - downloaded if total and total > downloaded else 0
                    eta_sec = int(remaining / speed) if speed > 0 and remaining > 0 else 0
                    eta_str = f"{eta_sec}s" if eta_sec else "-"
                    label_speed.config(text=_( "eta_label", lang_var.get()).format(speed=speed_mb, eta=eta_str))
                else:
                    label_speed.config(text="")
                if total and total > 0:
                    # determinate
                    pb.config(mode="determinate", maximum=total)
                    pb['value'] = downloaded
                else:
                    # indeterminate
                    if pb['mode'] != 'indeterminate':
                        pb.config(mode='indeterminate')
                        pb.start(10)
            except Exception:
                logging.exception("progress_cb GUI update failed")

        def runner():
            """Thread runner to call download_iso and handle post-download actions."""
            ok = download_iso(iso_url, save_path, lang_var.get(), progress_callback=progress_cb, stop_event=stop_event)
            # stop indeterminate if needed
            try:
                if pb['mode'] == 'indeterminate':
                    pb.stop()
                    pb.config(mode='determinate')
            except Exception:
                pass

            # restore UI state
            downloading.clear()
            btn_download.config(state="normal")
            btn_refresh.config(state="normal")
            btn_choose_folder.config(state="normal")
            mirror_list.config(state="normal")
            lang_menu.config(state="readonly")
            verify_var.config(state="normal")
            btn_cancel.config(state="disabled")
            btn_pause.config(state="disabled")
            btn_pause.config(text=_( "pause", lang_var.get()))
            pb['value'] = pb['maximum'] if ok else 0

            if ok:
                logging.info("Downloaded: %s from %s", save_path, mirror_url)
                label_status.config(text=_( "download_complete", lang_var.get()).format(os.path.basename(save_path)))
                # open folder button enabled
                btn_open_folder.config(state="normal")
            else:
                if stop_event and stop_event.is_set():
                    label_status.config(text="Cancelled")
                else:
                    label_status.config(text=_( "download_failed", lang_var.get()))

        download_thread = threading.Thread(target=runner, daemon=True)
        download_thread.start()

    def cancel_download():
        """Signal download thread to stop; download can be resumed later because resume is supported."""
        if messagebox.askyesno("", _( "cancel", lang_var.get())):
            if stop_event:
                stop_event.set()

    def pause_resume():
        """
        Pause implemented as cancel (stop_event). Resume achieved by clicking Download again:
        Because file is partially saved, download_iso will attempt Range resume.
        """
        if btn_pause.cget("text") == _( "pause", lang_var.get()):
            # pause -> set stop event
            if stop_event:
                stop_event.set()
            btn_pause.config(text=_( "resume", lang_var.get()))
            label_status.config(text="Paused")
        else:
            btn_pause.config(text=_( "pause", lang_var.get()))
            label_status.config(text="")
            # user should press Download to resume (we don't auto-restart)

    def show_help():
        """Display help panel with links to tools for creating bootable USBs."""
        messagebox.showinfo(_( "show_help", lang_var.get()), _( "help_text", lang_var.get()))

    def open_folder_btn():
        """Open last save folder in explorer."""
        folder = save_folder_var.get()
        open_folder(folder)

    # helper functions to open the official tool pages
    def open_rufus():
        """Open Rufus website in the default browser."""
        try:
            webbrowser.open("https://rufus.ie")
        except Exception:
            logging.exception("Failed to open Rufus link")

    def open_balena():
        """Open balenaEtcher website in the default browser."""
        try:
            webbrowser.open("https://www.balena.io/etcher/")
        except Exception:
            logging.exception("Failed to open balenaEtcher link")

    def update_ui_texts():
        """Update all visible UI text immediately to the selected language."""
        lang_now = lang_var.get()
        try:
            root.title(_( "gui_title", lang_now))
            label_country.config(text=_( "detected_country", lang_now).format(country_var.get() or ""))
            btn_download.config(text=_( "gui_download", lang_now))
            btn_refresh.config(text=_( "mirror_testing", lang_now))
            btn_choose_folder.config(text=_( "gui_choose", lang_now))
            help_btn.config(text=_( "show_help", lang_now))
            btn_open_folder.config(text=_( "open_folder", lang_now))
            btn_quit.config(text=_( "gui_quit", lang_now))
            btn_cancel.config(text=_( "cancel", lang_now))
            btn_pause.config(text=_( "pause", lang_now))
            # re-render mirror list entries using the current language (speed label localized)
            mirror_list.delete(0, tk.END)
            for i, m in enumerate(mirrors):
                mirror_list.insert(
                    tk.END,
                    f"{m['url']} ({m.get('protocol')}) - " + _( "mirror_speed_label", lang_now).format(
                        speeds[i] if i < len(speeds) else 0.0
                    ),
                )
            # clear status/speed text so they are consistent with new language
            label_speed.config(text="")
            label_status.config(text="")
        except Exception:
            logging.exception("update_ui_texts failed")

    def on_lang_change(*_):
        """Persist language selection and immediately update all UI texts."""
        persist_settings()
        update_ui_texts()

    # Build UI
    top_frame = tk.Frame(root, pady=8)
    top_frame.pack(fill="x")
    label_country = tk.Label(top_frame, text=_( "detecting_country", lang_var.get()))
    label_country.pack(side="left", padx=8)
    lang_menu = ttk.Combobox(top_frame, textvariable=lang_var, values=list(LANGUAGES.keys()), width=8, state="readonly")
    lang_menu.pack(side="right", padx=8)
    lang_menu.bind("<<ComboboxSelected>>", on_lang_change)

    main_frame = tk.Frame(root, padx=10, pady=6)
    main_frame.pack(fill="both", expand=True)
    mirror_list = tk.Listbox(main_frame, height=14)
    mirror_list.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=mirror_list.yview)
    scrollbar.pack(side="right", fill="y")
    mirror_list.config(yscrollcommand=scrollbar.set)

    action_frame = tk.Frame(root, pady=8)
    action_frame.pack(fill="x")
    btn_refresh = tk.Button(action_frame, text=_( "mirror_testing", lang_var.get()), command=lambda: threading.Thread(target=refresh_mirrors, daemon=True).start())
    btn_refresh.pack(side="left", padx=5)
    btn_choose_folder = tk.Button(action_frame, text=_( "gui_choose", lang_var.get()), command=choose_folder)
    btn_choose_folder.pack(side="left", padx=5)
    folder_entry = tk.Entry(action_frame, textvariable=save_folder_var, width=50)
    folder_entry.pack(side="left", padx=5)
    btn_download = tk.Button(action_frame, text=_( "gui_download", lang_var.get()), command=start_download, state="disabled")
    btn_download.pack(side="left", padx=5)
    # verify option removed
    help_btn = tk.Button(action_frame, text=_( "show_help", lang_var.get()), command=show_help)
    help_btn.pack(side="left", padx=5)
    # Buttons to open Rufus and balenaEtcher directly
    btn_rufus = tk.Button(action_frame, text="Rufus", command=open_rufus)
    btn_rufus.pack(side="left", padx=5)
    btn_balena = tk.Button(action_frame, text="balenaEtcher", command=open_balena)
    btn_balena.pack(side="left", padx=5)
    btn_open_folder = tk.Button(action_frame, text=_( "open_folder", lang_var.get()), command=open_folder_btn, state="disabled")
    btn_open_folder.pack(side="left", padx=5)
    btn_quit = tk.Button(action_frame, text=_( "gui_quit", lang_var.get()), command=lambda: (persist_settings(), root.quit()))
    btn_quit.pack(side="left", padx=5)

    ctrl_frame = tk.Frame(root)
    ctrl_frame.pack(fill="x", pady=6)
    btn_cancel = tk.Button(ctrl_frame, text=_( "cancel", lang_var.get()), command=cancel_download, state="disabled")
    btn_cancel.pack(side="left", padx=6)
    btn_pause = tk.Button(ctrl_frame, text=_( "pause", lang_var.get()), command=pause_resume, state="disabled")
    btn_pause.pack(side="left", padx=6)
    btn_save_settings = tk.Button(ctrl_frame, text="Save settings", command=persist_settings)
    btn_save_settings.pack(side="right", padx=6)

    pb = ttk.Progressbar(root, orient="horizontal", length=760, mode="determinate")
    pb.pack(pady=6)
    label_speed = tk.Label(root, text="", anchor="w")
    label_speed.pack(fill="x", padx=10)
    label_status = tk.Label(root, text="", anchor="w")
    label_status.pack(fill="x", padx=10, pady=4)

    # apply initial language to all widgets immediately
    update_ui_texts()

    # Start mirror refresh in background
    threading.Thread(target=refresh_mirrors, daemon=True).start()
    root.mainloop()

# -----------------------
# Program entry
# -----------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arch Linux ISO Downloader")
    parser.add_argument("--cli", action="store_true", help="Run in command-line mode")
    parser.add_argument("--lang", default=None, choices=list(LANGUAGES.keys()), help="Language")
    args = parser.parse_args()
    try:
        if args.cli:
            main_cli(args)
        else:
            main_gui()
    except Exception:
        logging.exception("Fatal error")
        raise