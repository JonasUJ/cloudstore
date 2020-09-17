document.addEventListener('DOMContentLoaded', function () {
    let files_app = new Vue({
        el: '#items-section',
        data: {
            cache: {},
            user: null,
            files: [],
            folders: [],
            sorting: 'Name',
            sortingTypes: ['Name', 'Size', 'Date'],
            ascending: true,
            breadcrumb: [],
            folder: false,
            target: null,
            edit: null,
            modal: {
                edit: null,
                newFolder: null
            },
            dragging: false,
            dragcur: null,
            dragsrc: null,
            uploading: false,
            type: 'file',
            upload_queue: {
                uploading: [],
                completed: [],
            },
        },
        computed: {
            sortedFiles: function () {
                return this.sorted(this.files, this.sorting, this.ascending);
            },
            sortedFolders: function () {
                return this.sorted(this.folders, this.sorting, this.ascending);
            },
            showModal: function () {
                // The modal should be shown if any of its properties is true
                for (let p in this.modal) {
                    if (this.modal[p]) {
                        return true;
                    }
                }
                return false;
            },
        },
        methods: {
            typeOf(obj) {
                return obj.hasOwnProperty('file') ? 'file' : 'folder'
            },
            removeFrom(obj, arr, func) {
                const index = arr.map(func).indexOf(obj.id);

                // If it isn't there to begin with, no need to remove it.
                if (index >= 0) {
                    arr.splice(index, 1);
                }
            },
            tiles() {
                return this.user?.settings.view === 'tiles';
            },
            hideModal() {
                // The modal is hidden if all of its properties is false/null
                for (let p in this.modal) {
                    this.modal[p] = null
                }
            },
            folderSize: (folder) => folder.files.length + folder.folders.length,
            direction: (bool, asc) => (bool * 2 - 1) * (asc * 2 - 1),
            sorted(list, key, ascending) {
                let res;
                let type;

                if (list[0]) {
                    type = this.typeOf(list[0]);
                } else {
                    return list.slice();
                }

                if (key === 'Name') {
                    res = list.slice().sort((a, b) => this.direction(a.name.toUpperCase() > b.name.toUpperCase(), ascending));
                } else if (key === 'Size') {
                    if (type === 'file') {
                        res = list.slice().sort((a, b) => this.direction(a.size > b.size, ascending));
                    } else {
                        res = list.slice().sort((a, b) => this.direction(this.folderSize(a) > this.folderSize(b), ascending));
                    }
                } else if (key === 'Date') {
                    if (type === 'file') {
                        res = list.slice().sort((a, b) => this.direction(a.accessed > b.accessed, ascending));
                    } else {
                        res = list.slice();
                    }
                } else {
                    res = list.slice();
                }

                return res;
            },
            setSorting(key) {
                // Switch direction if this key is already selected
                if (this.sorting === key) {
                    this.ascending = !this.ascending;
                }
                this.sorting = key;
            },
            purge(obj) {
                if (this.typeOf(obj) === 'file') {
                    // Files only need to be purged from their parent folder.
                    if (obj.folder in this.cache) {
                        this.removeFrom(obj, this.cache[obj.folder].files, f => f);
                        this.removeFrom(obj, this.cache[obj.folder].files_cache, f => f.id);
                    }
                } else {
                    // Folders need to also purge all their contents
                    if (obj.id in this.cache) {
                        for (const folder of this.cache[obj.id].folders_cache) {
                            if (folder.id in this.cache) {
                                this.purge(folder);
                            }
                        }
                        delete this.cache[obj.id];
                    }
                    if (obj.folder in this.cache) {
                        this.removeFrom(obj, this.cache[obj.folder].folders, f => f);
                        this.removeFrom(obj, this.cache[obj.folder].folders_cache, f => f.id);
                    }
                }
            },
            cacheFile(file, folder) {
                // If it is already cached, remove it to avoid duplicates.
                this.purge(file);

                // Insert it into the folder.
                if (folder in this.cache) {
                    this.cache[folder].files.push(file.id);
                    this.cache[folder].files_cache.push(file);
                }
            },
            cacheFolder(folder, parent) {
                // If it is already cached, remove it to avoid duplicates.
                this.purge(folder);

                // Ensure that the files_cache/folder_cache attributes are present.
                // We want to rely on this to avoid always checking.
                folder.files_cache = folder.files_cache || [];
                folder.folders_cache = folder.folders_cache || [];

                // Insert it into the folder
                if (parent in this.cache) {
                    this.cache[parent].folders.push(folder.id);
                    this.cache[parent].folders_cache.push(folder);
                }

                // Register in cache
                this.cache[folder.id] = folder;
            },
            async verify(obj, parent) {
                let type = this.typeOf(obj);
                let new_obj;
                try {
                    new_obj = await fetchData(`/api/${type}s/${obj.id}/`, {}, 'GET');
                } catch (resp) {
                    // If it was deleted
                    if (resp.status == 404) {
                        this.purge(obj);
                        return false;
                    }
                }

                // We want to purge the object if it has moved since it was cached.
                if (new_obj.folder !== parent) {
                    this.purge(obj);
                    return false;
                }

                return true;
            },
            async setBreadcrumb(folder, _recur=false) {
                // _recur shouldn't be passed from outside.
                // We clear the breadcrumb so that we can add a new
                if (!_recur) {
                    this.breadcrumb = [];
                }

                // We reached the end, time to terminate the recursion
                if (folder.folder === null) {
                    folder.name = 'Home';
                    this.breadcrumb.push(folder);
                    return;
                }

                this.breadcrumb.push(folder);
                if (folder.folder in this.cache) {
                    await this.setBreadcrumb(this.cache[folder.folder], true);
                } else {
                    const pk = this.folder.id;
                    // It wasn't in the cache meaning we have to fetch it.
                    const parent = await fetchData(`/api/folders/${folder.folder}/`, {}, 'GET');

                    // The folder has changed, making this breadcrumb outdated
                    if (pk !== this.folder.id) {
                        return;
                    }

                    this.cacheFolder(parent);
                    await this.setBreadcrumb(parent, true);
                }
            },
            async setFolder(pk=null) {
                let folderpk = pk;

                // Find the pk if none was passed
                if (pk === null) {
                    const params = new URLSearchParams(location.search);
                    folderpk = params.get('pk') || get('base_folder');
                }

                if (folderpk in this.cache) {
                    // Load from cache
                    this.folder = this.cache[folderpk];
                } else {
                    try {
                        // Load from API and cache it
                        this.folder = await fetchData(`/api/folders/${folderpk}/`, {}, 'GET');
                        this.cacheFolder(this.folder, this.folder.folder);
                    } catch (resp) {
                        // If a non-200 response status was returned it was probably because
                        // the folder didn't exist.
                        // Try with the base folder
                        let base_folder = get('base_folder');

                        // Check that haven't tried the base folder already to avoid
                        // endless recursion
                        if (pk != base_folder) {
                            await this.setFolder(base_folder);
                        }
                    }
                }

                // Update breadcrumb for the new folder
                await this.setBreadcrumb(this.folder);
            },
            async refresh() {
                const pk = this.folder.id;

                // Set these while we wait for the request to finish
                this.files = this.cache[this.folder.id].files_cache;
                this.folders = this.cache[this.folder.id].folders_cache;;

                // Get folder and contents
                const folder = await fetchData(`/api/folders/${this.folder.id}/contents/`, {}, 'GET');

                folder.files.forEach(f => {
                    f.created = new Date(f.created);
                    f.accessed = new Date(f.accessed);
                });

                // Check that we still want to refresh (the user might have navigated elsewhere)
                if (this.folder.id !== pk) {
                    return;
                }

                // Cache all loaded contents
                this.cache[folder.id].files_cache = folder.files;
                this.cache[folder.id].folders_cache = folder.folders;

                // Set references to the caches again
                this.files = this.cache[folder.id].files_cache;
                this.folders = this.cache[folder.id].folders_cache;
            },
            async openFolder(pk) {
                // Set the folder pk in the url for easy copy/paste
                const params = new URLSearchParams(location.search);
                params.set('pk', pk);
                window.history.pushState({pk:pk}, '', `${location.pathname}?${params.toString()}`);

                // Open the folder with this pk
                await this.setFolder(pk);
                await this.refresh();
            },
            isDisplayable(ext) {

                // If the file is an image type
                if (ext.length > 0) {
                    return imgtypes.includes(ext.substring(1).toUpperCase());
                }

                return false;
            },
            getIconClass(ext) {

                // Return an icon class based in the filetype
                if (ext.length > 0) {
                    if (filetypes.includes(ext.substring(1).toUpperCase())) {
                        return `fiv-icon-${ext.substring(1).toLowerCase()}`
                    }
                }

                // Default
                return 'fiv-icon-blank'
            },
            dragenter(e) {
                // Remove the is-active class and add it to the new element
                if (this.dragcur) {
                    this.dragcur.classList.remove('is-active');
                }
                this.dragcur = e.currentTarget;
                this.dragcur.classList.add('is-active');
            },
            async dragend(e, obj, parent) {
                this.dragging = false;

                // It's unlikely that whatever operation is taking place has already finished.
                // But we really want to verify the obj here, so we just check a couple of times.
                if (await this.verify(obj, parent)) {
                    setTimeout(async () => {
                        if (await this.verify(obj, parent)) {
                            setTimeout(async () => await this.verify(obj, parent), 1000);
                        }
                    }, 300);
                }
            },
            drag(e, obj, type) {
                this.dragsrc = e.currentTarget;
                e.dataTransfer.effectAllowed = 'move';

                // Set the name and truncate it
                let name = obj.name;
                if (name.length > 12) {
                    name = `${name.substring(0, 12)}...`;
                }

                this.dragging = name;
                this.type = type;

                e.dataTransfer.setData('application/json', JSON.stringify(obj));

                // Give Vue a chance to update the .drag element before setting it as the image
                Vue.nextTick(() => {
                    const elem = document.getElementsByClassName('drag').item(0);
                    e.dataTransfer.setDragImage(elem, 10, 10);
                });
            },
            async drop(e, folder) {
                e.currentTarget.classList.remove('is-active')
                this.dragcur = null;

                // This check makes sure we don't try to add a folder to itself
                if (e.currentTarget !== this.dragsrc) {
                    const data = e.dataTransfer.getData('application/json');

                    if (data) {
                        let obj = JSON.parse(data);
                        if (this.typeOf(obj) === 'file') {
                            // We can't have duplicate keys.
                            // Besides, if it is already there == job done.
                            if (!folder.files.includes(obj.id)) {
                                await this.handleFile(obj, obj.name, folder.id);
                            }
                        } else {
                            // Same as above
                            if (!folder.folders.includes(obj.id)) {
                                await this.handleFolder(obj, obj.name, folder.id);
                            }
                        }
                    } else {

                        for (const item of e.dataTransfer.items) {
                            // Forwards compatibility
                            item.getAsEntry = item.getAsEntry || item.webkitGetAsEntry;

                            const entry = item.getAsEntry();
                            if (entry.isFile) {
                                await this.handleFile(entry, entry.name, folder.id);
                            } else if (entry.isDirectory) {
                                // We add the parent here because handleFolder dumps the contents
                                // in the folder we specify, and we don't want it in `folder`.
                                const parent = await fetchData('/api/folders/', {
                                    name: entry.name,
                                    folder: folder.id,
                                }, 'POST');
                                this.cacheFolder(parent, folder.id);
                                await this.handleFolder(entry, entry.name, parent.id);
                            }
                        }
                    }
                }
            },
            async deleteObj(obj) {
                // We purge it first to give the impression that the operation was instant.
                // The request will still happen in the background.
                this.purge(obj);
                await fetchData(`/api/${this.typeOf(obj)}s/${obj.id}/`, {}, 'DELETE');
            },
            abortAll() {
                this.upload_queue.uploading.slice().forEach(f => f.xhr.abort())
            },
            async _handle(f, name, folder) {
                // Add file to the upload queue
                const file_upload = {
                    id: randomString(8),
                    name: name,
                    progress: 0,
                    xhr: null,
                }
                this.upload_queue.uploading.push(file_upload);

                // Upload the file
                file_upload.xhr = XHRFetch('/api/files/', {
                    name: name,
                    folder: folder,
                    file: f,
                }, 'POST',
                (resp, err) => { // onload
                    if (err) { throw err }
                    const new_file = JSON.parse(resp);
                    new_file.created = new Date(new_file.created);
                    new_file.accessed = new Date(new_file.accessed);

                    // Cache the new file
                    this.cacheFile(new_file, folder);

                    // Move file_upload from uploading to completed
                    this.removeFrom(file_upload, this.upload_queue.uploading, o => o.id);
                    this.upload_queue.completed.push(file_upload);
                }, (e) => { // onprogress
                    file_upload.progress = e.loaded / e.total * 100;
                }, () => { // onabort
                    this.removeFrom(file_upload, this.upload_queue.uploading, o => o.id);
                })
            },
            async handleFile(file, name = null, folder = null) {
                name = name ?? file.name;
                folder = folder ?? this.folder.id;

                // If this is a `file` from the API or an entry
                if (file.hasOwnProperty('id')){
                    // If it's a `file`, change it's name and move it to the new folder.
                    const new_file = await fetchData(`/api/files/${file.id}/`, {
                        name: name,
                        folder: folder,
                    }, 'PUT');

                    new_file.created = new Date(new_file.created);
                    new_file.accessed = new Date(new_file.accessed);

                    // Update it in the cache
                    this.purge(file);
                    this.cacheFile(new_file, folder);

                } else {

                    // We already know it is a file, but not whether it is a File or a FileEntry.
                    // Only file entries has .isFile and it will be undefined (false) on Files
                    if (file.isFile) {
                        // .file makes a File object out of the entry
                        await file.file(async (f) => await this._handle(f, name, folder));
                    } else {
                        await this._handle(file, name, folder);
                    }


                }
            },
            async handleFolder(folder, name, parent) {
                // If this is a `folder` from the API or an entry
                if (folder.hasOwnProperty('id')) {
                    // Update it through the API
                    const new_folder = await fetchData(`/api/folders/${folder.id}/`, {
                        name: name,
                        folder: parent,
                    }, 'PUT');

                    // Update it in the cache
                    this.cacheFolder(new_folder, new_folder.folder);

                } else {
                    // Read the entries of the folder entry
                    let reader = folder.createReader();
                    reader.readEntries(async (entries) => {

                        for (const entry of entries) {
                            if (entry.isFile) {
                                await this.handleFile(entry, entry.name, parent);

                            } else if (entry.isDirectory) {
                                // If it is a folder we want to create a folder for it
                                // and pass it to handleFolder again to recursivly unpack the entry
                                const nested_folder = await fetchData('/api/folders/', {
                                    name: entry.name,
                                    folder: parent,
                                }, 'POST');

                                // Cache the new folder under the parent
                                this.cacheFolder(nested_folder, parent);

                                // Recursive call
                                await this.handleFolder(entry, entry.name, nested_folder.id)
                            }
                        }
                    });
                }
            },
            async newFolder() {
                // Create new folder
                const new_folder = await fetchData('/api/folders/', {
                    name: get('new-folder'),
                    folder: this.folder.id,
                });

                // Cache it after creation
                this.cacheFolder(new_folder, this.folder.id);
                this.modal.newFolder = false;
            },
            async editName() {
                if (this.typeOf(this.modal.edit) === 'file') {
                    await this.handleFile(this.modal.edit, get('edit-name'), this.modal.edit.folder)
                    this.modal.edit = null;
                } else {
                    await this.handleFolder(this.modal.edit, get('edit-name'), this.modal.edit.folder)
                    this.modal.edit = null;
                }
            },
            async switchView() {
                let new_view = this.tiles() ? 'list' : 'tiles';
                this.user.settings.view = new_view;

                // It's ugly, but that's not enough reason to create a new endpoint for it
                await fetchData('/account/', {
                    'form_settings-view': new_view,
                    'form_settings-view_img': this.user.settings.view_img,
                    'form_settings-show_ext': this.user.settings.show_ext,
                });
            },
            // Debug logging for use in the templates
            log(any) {
                console.log(any);
            }
        },
        async mounted() {
            // Check if the `pk` parameter was passed.
            // If not, open the base folder instead.
            const params = new URLSearchParams(location.search);
            const pk = params.get('pk') || get('base_folder');
            window.history.replaceState({pk:pk}, '', location.href);

            // Get the current user
            this.user = await fetchData(`/api/users/${get('pk')}/`, {}, 'GET')

            // Update page
            await this.setFolder(pk);
            await this.refresh();
        },
    });
    // We cache everything, so if the back or forwards button is pressed
    // we want to retain the cache.
    // This means we have to reload the page manually and set the GET parameters for easy
    // reloading/copy-pasting of the page.
    window.addEventListener('popstate', async (event) => {
        if (event.state !== null && event.state.pk !== null) {
            await files_app.setFolder(event.state.pk);
            await files_app.refresh();
        } else {
            const params = new URLSearchParams(location.search);
            window.history.replaceState({pk:params.get('pk') || get('base_folder')}, '', location.href);
        }
    });
    // We want to warn the user if they leave the page while an upload is in progress
    window.addEventListener('beforeunload', (event) => {
        if (files_app.uploading) {
            event.preventDefault();
            event.returnValue = '';
        } else {
            delete event['returnValue'];
        }
    });
});
