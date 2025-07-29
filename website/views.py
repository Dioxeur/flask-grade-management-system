from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from website.models import Note, Subject, Grade, User
from website.forms import NoteForm, SubjectForm, AddGradeForm
from website import db


views = Blueprint('views', __name__)
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if current_user.role == 'teacher':
        return redirect(url_for('views.teacher_dashboard'))
    elif current_user.role == 'student':
        return redirect(url_for('views.student_dashboard'))
    
    # Default note functionality with secure form
    form = NoteForm()
    if form.validate_on_submit():
        new_note = Note(data=form.note.data, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note added successfully!', category='success')
        return redirect(url_for('views.home'))
    
    return render_template("home.html", user=current_user, form=form)

@views.route('/teacher-dashboard')
@login_required
def teacher_dashboard():
    if current_user.role != 'teacher':
        flash('Access denied. Teachers only.', category='error')
        return redirect(url_for('views.home'))
    
    subjects = Subject.query.filter_by(teacher_id=current_user.id).all()
    return render_template("teacher_dashboard.html", user=current_user, subjects=subjects)

@views.route('/student-dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash('Access denied. Students only.', category='error')
        return redirect(url_for('views.home'))
    
    grades = Grade.query.filter_by(student_id=current_user.id).all()
    return render_template("student_dashboard.html", user=current_user, grades=grades)

@views.route('/create-subject', methods=['GET', 'POST'])
@login_required
def create_subject():
    if current_user.role != 'teacher':
        flash('Access denied. Teachers only.', category='error')
        return redirect(url_for('views.home'))
    
    form = SubjectForm()
    if form.validate_on_submit():
        new_subject = Subject(
            name=form.name.data, 
            code=form.code.data.upper(), 
            teacher_id=current_user.id
        )
        db.session.add(new_subject)
        db.session.commit()
        flash('Subject created successfully!', category='success')
        return redirect(url_for('views.teacher_dashboard'))
    
    return render_template("create_subject.html", user=current_user, form=form)

@views.route('/add-grade/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def add_grade(subject_id):
    if current_user.role != 'teacher':
        flash('Access denied. Teachers only.', category='error')
        return redirect(url_for('views.home'))
    
    subject = Subject.query.get_or_404(subject_id)
    if subject.teacher_id != current_user.id:
        flash('You can only add grades to your own subjects.', category='error')
        return redirect(url_for('views.teacher_dashboard'))
    
    form = AddGradeForm()
    if form.validate_on_submit():
        new_grade = Grade(
            value=float(form.value.data),
            max_value=float(form.max_value.data),
            student_id=form.student_id.data,
            subject_id=subject_id,
            teacher_id=current_user.id
        )
        db.session.add(new_grade)
        db.session.commit()
        flash('Grade added successfully!', category='success')
        return redirect(url_for('views.teacher_dashboard'))
    
    return render_template("add_grade.html", user=current_user, subject=subject, form=form)

@views.route('/delete/<int:id>/', methods=['GET', 'POST'])
@login_required
def delete(id):
    note = Note.query.get_or_404(id)
    
    # Security check: only allow users to delete their own notes
    if note.user_id != current_user.id:
        flash('You can only delete your own notes.', category='error')
        return redirect(url_for('views.home'))
    
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted successfully!', category='success')
    return redirect(url_for('views.home'))

@views.route('/')
def Home():
    all_data = Note.query.all()
    return render_template("home.html", employees=all_data)

@views.route('/switch-role')
@login_required
def switch_role():
    if current_user.role == 'student':
        current_user.role = 'teacher'
        flash('Switched to Teacher role!', category='success')
    else:
        current_user.role = 'student'
        flash('Switched to Student role!', category='success')
    
    db.session.commit()
    return redirect(url_for('views.home'))

@views.route('/manage-grades/<int:subject_id>')
@login_required
def manage_grades(subject_id):
    if current_user.role != 'teacher':
        flash('Access denied. Teachers only.', category='error')
        return redirect(url_for('views.home'))
    
    subject = Subject.query.get_or_404(subject_id)
    if subject.teacher_id != current_user.id:
        flash('You can only manage grades for your own subjects.', category='error')
        return redirect(url_for('views.teacher_dashboard'))
    
    grades = Grade.query.filter_by(subject_id=subject_id, teacher_id=current_user.id).all()
    return render_template("manage_grades.html", user=current_user, subject=subject, grades=grades)

@views.route('/edit-grade/<int:grade_id>', methods=['GET', 'POST'])
@login_required
def edit_grade(grade_id):
    if current_user.role != 'teacher':
        flash('Access denied. Teachers only.', category='error')
        return redirect(url_for('views.home'))
    
    grade = Grade.query.get_or_404(grade_id)
    if grade.teacher_id != current_user.id:
        flash('You can only edit your own grades.', category='error')
        return redirect(url_for('views.teacher_dashboard'))
    
    if request.method == 'POST':
        grade.value = float(request.form.get('value'))
        grade.max_value = float(request.form.get('max_value'))
        db.session.commit()
        flash('Grade updated successfully!', category='success')
        return redirect(url_for('views.manage_grades', subject_id=grade.subject_id))
    
    return render_template("edit_grade.html", user=current_user, grade=grade)

@views.route('/delete-grade/<int:grade_id>')
@login_required
def delete_grade(grade_id):
    if current_user.role != 'teacher':
        flash('Access denied. Teachers only.', category='error')
        return redirect(url_for('views.home'))
    
    grade = Grade.query.get_or_404(grade_id)
    if grade.teacher_id != current_user.id:
        flash('You can only delete your own grades.', category='error')
        return redirect(url_for('views.teacher_dashboard'))
    
    subject_id = grade.subject_id
    db.session.delete(grade)
    db.session.commit()
    flash('Grade deleted successfully!', category='success')
    return redirect(url_for('views.manage_grades', subject_id=subject_id))


