from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from app import db
from app.models import Summary
from app.summarizer import ArticleSummarizer
from app.forms import SummarizationForm
import time
from datetime import datetime

main_bp = Blueprint('main', __name__)

# Initialize the summarizer
summarizer = ArticleSummarizer()


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    form = SummarizationForm()
    summary = None
    original_text = ""
    processing_time = 0
    url = ""
    title = ""

    if form.validate_on_submit():
        start_time = time.time()

        # Get form data
        url = form.url.data
        original_text = form.text.data
        title = form.title.data
        min_length = form.min_length.data
        max_length = form.max_length.data
        save_summary = form.save_summary.data

        # If URL is provided, extract text
        if url:
            original_text = summarizer.extract_text_from_url(url)
            if original_text.startswith("Error"):
                flash(original_text, 'danger')
                return render_template('index.html', form=form, title="Home")

            # Extract title from URL if not provided
            if not title and url:
                try:
                    import requests
                    from bs4 import BeautifulSoup
                    response = requests.get(url, timeout=10)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.title.string if soup.title else url.split('/')[-1]
                except:
                    title = url.split('/')[-1]

        # Generate summary
        if original_text:
            summary = summarizer.summarize_long_text(
                original_text,
                max_length=max_length,
                min_length=min_length
            )

            processing_time = round(time.time() - start_time, 2)

            # Calculate statistics
            original_word_count = len(original_text.split())
            summary_word_count = len(summary.split())
            compression = round((summary_word_count / original_word_count) * 100, 1) if original_word_count > 0 else 0

            # Save to database if user is logged in and wants to save
            if current_user.is_authenticated and save_summary:
                new_summary = Summary(
                    title=title or f"Summary from {datetime.utcnow().strftime('%Y-%m-%d')}",
                    original_text=original_text,
                    summary_text=summary,
                    url=url or None,
                    user_id=current_user.id,
                    original_length=original_word_count,
                    summary_length=summary_word_count,
                    compression_ratio=compression / 100,
                    processing_time=processing_time
                )

                # Save parameters
                new_summary.set_parameters({
                    'min_length': min_length,
                    'max_length': max_length
                })

                db.session.add(new_summary)
                db.session.commit()
                flash('Summary saved to your history!', 'success')

    return render_template('index.html',
                           form=form,
                           summary=summary,
                           original_text=original_text,
                           processing_time=processing_time,
                           url=url,
                           title="Home")


@main_bp.route('/about')
def about():
    return render_template('about.html', title="About")


@main_bp.route('/history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['SUMMARIES_PER_PAGE']

    summaries = Summary.query.filter_by(user_id=current_user.id) \
        .order_by(Summary.created_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('history.html',
                           title="My Summaries",
                           summaries=summaries)


@main_bp.route('/summary/<int:id>')
@login_required
def view_summary(id):
    summary = Summary.query.get_or_404(id)

    # Check if the summary belongs to the current user
    if summary.user_id != current_user.id:
        flash('You are not authorized to view this summary.', 'danger')
        return redirect(url_for('main.history'))

    return render_template('summary.html',
                           title=summary.title,
                           summary=summary)


@main_bp.route('/summary/delete/<int:id>')
@login_required
def delete_summary(id):
    summary = Summary.query.get_or_404(id)

    # Check if the summary belongs to the current user
    if summary.user_id != current_user.id:
        flash('You are not authorized to delete this summary.', 'danger')
        return redirect(url_for('main.history'))

    db.session.delete(summary)
    db.session.commit()

    flash('Summary has been deleted.', 'success')
    return redirect(url_for('main.history'))