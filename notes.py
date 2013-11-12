import os, datetime
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for, jsonify
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from jinja2 import TemplateNotFound

import models
from libs.User import User
import random, string

notes_app = Blueprint('notes_app', __name__, template_folder='templates')

@notes_app.route('/')
def index():
	templateData = {
		'notes' : models.Note.objects.order_by("-last_updated")
	}
	return render_template('index.html', **templateData)



@notes_app.route("/notes/create", methods=["GET","POST"])
@login_required
def admin_entry_create():

	if request.method == "POST":
		entry = models.Note()
		entry.title = request.form.get('title','')
		entry.content = request.form.get('content')

		# associate note to currently logged in user
		entry.user = current_user.get_mongo_doc()
		entry.save()

		
		return redirect('/notes/%s' % entry.id)

	else:
		template_data = {
			'title' : 'Create new note',
			'entry' : None
		}
		return render_template('/note_edit.html', **template_data)


@notes_app.route("/notes/<note_id>/edit", methods=["GET","POST"])
@login_required
def admin_entry_edit(note_id):

	# get single document returned
	entry = models.Note.objects().with_id(note_id)

	if entry:
		if entry.user.id != current_user.id:
			return "Sorry you do not have permission to edit this note"

		if request.method == "POST":
			entry.title = request.form.get('title','')
			entry.content = request.form.get('content')
			
			entry.save()

		template_data = {
			'title' : 'Edit note',
			'entry' : entry
		}

		current_app.logger.debug(current_user.id)

		return render_template('/note_edit.html', **template_data)

	else:
		return "Unable to find entry %s" % note_id


@notes_app.route('/notes/<note_id>')
def entry_page(note_id):

	# get class notes entry with matching slug
	entry = models.Note.objects().with_id(note_id)

	if entry:
		templateData = {
			'entry' : entry
		}
		return render_template('note_display.html', **templateData)

	else:
		return "not found"




