document.addEventListener('DOMContentLoaded', function () {
    if (!document.getElementById('navbar')) {
        return;
    }

    var nav_app = new Vue({
        el: '#navbar',
        data: {
            accessToken: '',
            generatedResponseMessage: '',
            accessTokenModalActive: false,
            navbarActive: false,
            shared_state: shared_state,
        },
        methods: {
            async generate_access_token() {
                const data = await fetchData('/api/access_token/', {
                        token: randomString(10)
                    });
                if (data.token) {
                    this.generatedResponseMessage = 'Generated an access token';
                    this.accessToken = data.token;
                } else {
                    this.generatedResponseMessage =
                        'An error occurred when generating a token: ' + JSON.stringify(data);
                }
                this.accessTokenModalActive = true;
            },
            copyAccessToken() {
                copyToClipboard(this.accessToken);
            },
        }
    });
});