document.addEventListener('DOMContentLoaded', function () {
    async function handleFile(file, name, folder) {
        if (file.hasOwnProperty('id')){
            await fetchData(`/api/files/${file.id}/`, {
                name: name,
                folder: folder,
            }, 'PUT');
        } else {
            file.file(async (f) => {
                await fetchData(`/api/files/`, {
                    name: name,
                    folder: folder,
                    file: f,
                }, 'POST');
            });
        }
    }

    async function handleFolder(folder, name, parent) {
        if (folder.hasOwnProperty('id')) {
            return await fetchData(`/api/folders/${folder.id}/`, {
                name: name,
                parent: parent,
            }, 'PUT');
        } else {

        }
    }

    async function getFileTree(item, path = '') {
        if (item.isFile) {

            item.file(function(file) {
                console.log(path + file.name);
            });

        } else if (item.isDirectory) {

            console.log(item);

            // Get folder contents
            var dirReader = item.createReader();
            dirReader.readEntries(async (entries) => {
                for (const entry of entries) {
                    await getFileTree(entry, path + item.name + '/');
                }
            });
        }
    }

    let files_app = new Vue({
        el: '#items-section',
        data: {
            cache: {},
            files: false,
            folders: false,
            folder: false,
            dragging: false,
            dragcur: null,
            dragsrc: null,
            type: 'file',
        },
        methods: {
            async refresh() {
                await this.updateFolders();
                await this.updateFiles();
            },
            async setFolder(pk=null) {
                let folderpk = pk;
                if (pk === null) {
                    const params = new URLSearchParams(location.search);
                    folderpk = params.get('pk');
                    if (!folderpk) {
                        const user = await fetchData(`/api/users/${get('pk')}/`, {}, 'GET');
                        folderpk = user.base_folder;
                    }
                }

                if (this.cache.hasOwnProperty(folderpk)) {
                    this.folder = this.cache[folderpk];
                } else {
                    try {
                        this.folder = await fetchData(`/api/folders/${folderpk}/`, {}, 'GET');
                        this.cache[this.folder.id] = this.folder;
                    } catch (resp) {
                        let getpk = get('pk');

                        if (pk != getpk) {
                            await this.setFolder(getpk);
                        }
                    }
                }

            },
            async updateFiles() {
                if (this.cache.hasOwnProperty(this.folder.id) && this.cache[this.folder.id].hasOwnProperty('files_cache')) {
                    this.files = this.cache[this.folder.id].files_cache;
                } else {
                    const id = this.folder.id;
                    this.files = [];

                    for (const filepk of this.cache[id].files) {
                        const file = await fetchData(`/api/files/${filepk}/`, {}, 'GET');

                        if (id == this.folder.id) {
                            this.files.push(file);
                        } else {
                            return;
                        }
                    }

                    this.cache[this.folder.id].files_cache = this.files;
                }

                if (this.files.length === 0) {
                    this.files = false;
                }
            },
            async updateFolders() {
                if (this.cache.hasOwnProperty(this.folder.id) && this.cache[this.folder.id].hasOwnProperty('folders_cache')) {
                    this.folders = this.cache[this.folder.id].folders_cache;
                } else {
                    const id = this.folder.id;
                    this.folders = [];

                    for (const folderpk of this.cache[id].folders) {
                        const folder = await fetchData(`/api/folders/${folderpk}/`, {}, 'GET');

                        if (id == this.folder.id) {
                            this.folders.push(folder);
                        } else {
                            return;
                        }
                    }

                    this.cache[this.folder.id].folders_cache = this.folders;
                }

                if (this.folders.length === 0) {
                    this.folders = false;
                }
            },
            async openFolder(pk) {
                const params = new URLSearchParams(location.search);
                params.set('pk', pk);
                window.history.pushState({pk:pk}, '', `${location.pathname}?${params.toString()}`);
                await this.setFolder(pk);
                await this.refresh();
            },
            isDisplayable(ext) {
                if (ext.length > 0) {
                    return imgtypes.includes(ext.substring(1).toUpperCase());
                }

                return false;
            },
            getIconClass(ext) {
                if (ext.length > 0) {
                    if (filetypes.includes(ext.substring(1).toUpperCase())) {
                        return `fiv-icon-${ext.substring(1).toLowerCase()}`
                    }
                }

                return 'fiv-icon-gitignore'
            },
            dragenter(e) {
                e.currentTarget.classList.add('is-active');
                this.dragcur = e.target;
            },
            dragleave(e) {
                if (e.target === this.dragcur) {
                    e.currentTarget.classList.remove('is-active');
                }
            },
            drag(e, obj, type) {
                this.dragsrc = e.currentTarget;
                e.dataTransfer.effectAllowed = 'move';

                let name = obj.name;
                if (name.length > 16) {
                    name = `${name.substring(0, 16)}...`;
                }

                this.dragging = name;
                this.type = type;

                e.dataTransfer.setData('application/json', JSON.stringify(obj));

                Vue.nextTick(() => {
                    const elem = document.getElementsByClassName('drag').item(0);
                    e.dataTransfer.setDragImage(elem, 60, 30);
                });
            },
            async drop(e, folder) {
                e.currentTarget.classList.remove('is-active')
                this.dragcur = null;

                if (e.currentTarget !== this.dragsrc) {
                    const data = e.dataTransfer.getData('application/json');

                    if (data) {
                        let obj = JSON.parse(data);

                        if (obj.hasOwnProperty('file')) {
                            await handleFile(obj, obj.name, folder.id);
                        } else {
                            await handleFolder(obj, obj.name, folder.id);
                        }

                    } else {

                        console.log(e.dataTransfer.items[0].webkitGetAsEntry());
                        for (const item of e.dataTransfer.items) {
                            item.GetAsEntry = item.GetAsEntry || item.webkitGetAsEntry;
                            const entry = item.GetAsEntry();
                            if (entry.isFile) {
                                await handleFile(entry, entry.name, folder.id);
                            } else if (entry.isDirectory) {
                                await handleFolder(entry, entry.name, folder.id);
                            }
                        }
                    }
                }
            },
            log(any) {
                console.log(any);
            }
        },
        async mounted() {
            window.history.replaceState({pk:get('pk')}, '', location.href);
            await this.setFolder();
            await this.refresh();
        },
    });
    window.addEventListener('popstate', async function (event) {
        if (event.state !== null && event.state.pk !== null) {
            await files_app.setFolder(event.state.pk);
            await files_app.refresh();
        } else {
            window.history.replaceState({pk:get('pk')}, '', location.href);
        }
    });
});
