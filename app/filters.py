from flask import Markup
import hashlib


def register_filters(app):
    """Register custom template filters"""

    @app.template_filter('nl2br')
    def nl2br_filter(s):
        """Convert newlines to <br> tags"""
        if not s:
            return ""
        return Markup(s.replace('\n', '<br>'))

    @app.template_filter('md5')
    def md5_filter(s):
        """Convert string to MD5 hash (for Gravatar)"""
        if not s:
            return ""
        return hashlib.md5(s.encode()).hexdigest()