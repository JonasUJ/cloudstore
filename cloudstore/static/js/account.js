document.addEventListener('DOMContentLoaded', function () {
    var account_app = new Vue({
        el: '#account',
        data: {
            modalActive: false,
            deleteMsg: '',
        },
        methods: {
            async deleteAccount() {
                if (get('username') == get('confirm-username')) {
                    const data = await fetchData(`/api/users/${get('pk')}/`, {}, 'DELETE');
                    location.href = '../';
                    this.deleteMsg = data.detail;
                } else {
                    this.deleteMsg = 'Username didn\'t match';
                }
            },
        }
    });
});