from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import db
from app.models import User, Summary
from app.forms import LoginForm, RegistrationForm
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        user.update_last_seen()

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')

        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@auth_bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        current_user.update_last_seen()
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', title='Register', form=form)


@auth_bp.route('/profile')
@login_required
def profile():
    current_user.update_last_seen()
    summaries = current_user.summaries.order_by(Summary.created_at.desc()).all()
    summaries_count = len(summaries)

    # Calculate statistics
    stats = {
        'count': summaries_count,
        'total_words_original': 0,
        'total_words_summary': 0,
        'avg_compression': 0,
        'recent_summary': None
    }

    if summaries_count > 0:
        stats['recent_summary'] = summaries[0]
        total_compression = 0

        for summary in summaries:
            stats['total_words_original'] += summary.original_length
            stats['total_words_summary'] += summary.summary_length
            total_compression += summary.compression_ratio

        stats['avg_compression'] = round((total_compression / summaries_count) * 100, 1)

        # Get monthly summary counts for the chart
        from collections import defaultdict
        import datetime

        monthly_counts = defaultdict(int)
        for summary in summaries:
            month_key = summary.created_at.strftime('%Y-%m')
            monthly_counts[month_key] += 1

        # Get the last 6 months
        today = datetime.datetime.utcnow()
        months = []
        counts = []

        for i in range(5, -1, -1):
            month_date = today - datetime.timedelta(days=30*i)
            month_key = month_date.strftime('%Y-%m')
            month_label = month_date.strftime('%b %Y')
            months.append(month_label)
            counts.append(monthly_counts.get(month_key, 0))

        # Store the chart data directly
        stats['chart_months'] = months
        stats['chart_counts'] = counts

        # Assign height classes for the chart bars
        max_count = max(counts) if counts and max(counts) > 0 else 1

        # Map counts to height classes (height-0 through height-5)
        height_classes = []
        for count in counts:
            if count == 0:
                height_classes.append('height-0')
            elif count == max_count:
                height_classes.append('height-5')
            else:
                # Calculate relative height (1-4)
                relative_height = min(4, max(1, int((count / max_count) * 4) + 1))
                height_classes.append(f'height-{relative_height}')

        stats['chart_height_classes'] = height_classes

    return render_template('profile.html', title='Profile', user=current_user, stats=stats)


@auth_bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
