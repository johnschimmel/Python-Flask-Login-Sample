import os, datetime
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from jinja2 import TemplateNotFound
from app import login_manager, flask_bcrypt
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)

import models
import forms
# from libs.User import User

admin_pages = Blueprint('admin_pages', __name__, template_folder='templates')

@admin_pages.route('/', methods=["GET"])
@login_required
def admin_main():
	entries = models.ClassNote.objects().order_by('+class_date')
	pages = models.Page.objects()
	templateData = {
		'entries' : entries,
		'pages' : pages
	}	
	return render_template('/admin/index.html', **templateData)


@admin_pages.route('/entry', methods=["GET","POST"])
@login_required
def admin_create_entry():
	if request.method == "POST":
		entryData = {
			'title' : request.form.get('title',''),
			'url_title' : request.form.get('url_title',''),
			'description' : request.form.get('description',''),
			'published' : True if request.form['published'] == "true" else False,
			'github_url' : request.form.get('github_url',None),
			'demo_url' : request.form.get('demo_url',None),
			'content' : request.form.get('content'),
			'assignment' : request.form.get('assignment'),
			'class_date' : datetime.datetime.strptime(request.form.get('class_date'), "%Y-%m-%d")
		}

		entry = models.ClassNote(**entryData)

		try:
			entry.save()
			flash('Class entry:<b>%s</b> was saved' % entry.title)
			return redirect('/admin')

		except ValidationError:
			app.logger.error(ValidationError.errors)
			return "error on saving document"


	return render_template('/admin/entry_new.html')

@admin_pages.route("/entry/edit/<entry_id>", methods=["GET","POST"])
@login_required
def admin_entry_edit(entry_id):

	# get single document returned
	entry = models.ClassNote.objects().with_id(entry_id)

	if entry:
		if request.method == "POST":
			entry.title = request.form.get('title','')
			entry.url_title = request.form.get('url_title','')
			entry.description = request.form.get('description','')
			entry.published = True if request.form['published'] == "true" else False
			entry.github_url = request.form.get('github_url',None)
			entry.demo_url = request.form.get('demo_url',None)
			entry.content = request.form.get('content')
			entry.assignment = request.form.get('assignment')
			entry.class_date = datetime.datetime.strptime(request.form.get('class_date'), "%Y-%m-%d")

			entry.save()

		template_data = {
			'entry' : entry
		}

		return render_template('/admin/entry_edit.html', **template_data)

	else:
		return "Unable to find entry %s" % entry_id

@admin_pages.route("/page/<page_id>", methods=["GET","POST"])
@login_required
def admin_page_edit(page_id=None):

	

	if request.method=='GET':

		if page_id == 'new':
			pageForm = forms.page_form()
			template_data = {
				'form' : pageForm, 
				'page_id' : 'new'
			}
			
		else:
			try:
				page = models.Page.objects().get(id=page_id)
				if page:
					pageForm = forms.page_form(obj=page)
					template_data = {
						'form' : pageForm,
						'page_id' : page_id
					}
				
			except:
				return 'uhoh couldn\'t find it.'
			
				
		return render_template('admin/page_entry.html',**template_data)



	elif request.method=='POST':
		pageForm = forms.page_form(request.form)


		

		if pageForm.validate() and page_id == 'new':

			# create new page
			page = models.Page()
			pageForm.populate_obj(page)
			page.save()
			return redirect('/admin/page/' + str(page.id))

		elif pageForm.validate():

			# get the page
			page = models.Page.objects().get(id=page_id)
			if page:
				pageForm.populate_obj(page)
				page.save()
				template_data = {
					'form' : pageForm,
					'page_id' : page.id
				}
				return render_template('admin/page_entry.html', **template_data)

			else: 
				return "Valid form but unable to find page"
		else:

			template_data = {
				'form' : pageForm,
				'page_id' : request.form.get('page_id')
			}
			return render_template('admin/page_entry.html', **template_data)

@admin_pages.route('/remove_assignment/<class_id>/<assignment_id>')
@login_required
def remove_assignment_comment(class_id, assignment_id):

	try:
		notes = models.ClassNote.objects.with_id(class_id) #
		notes.update(pull__assignments___id=assignment_id)
		return redirect('/admin/edit/' + class_id)
		
	except:
		return "unable to fetch notes and assignment"
	
