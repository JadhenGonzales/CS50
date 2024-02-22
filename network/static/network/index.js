addEventListener('DOMContentLoaded', event => {load_posts()});

async function load_posts() {
    request = new Request('/show_posts',{
        method: 'GET'
    })
}