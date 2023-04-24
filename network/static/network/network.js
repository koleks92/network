document.addEventListener('DOMContentLoaded', function() {
    // Use buttons to toggle between views
    document.querySelector('#all_posts').addEventListener('click', () => load_page('all_posts'));
    document.querySelector('#profile').addEventListener('click', () => profile());
    document.querySelector('#following').addEventListener('click', () => load_page('following'));

    // By default, load the inbox
    load_page('all_posts');
});

function load_page(page) {
    // Show the load_page and hide other views
    document.querySelector('#load_page').style.display = 'block';
    document.querySelector('#profile').style.display = 'none';
}

function profile() {
    // Show the profile and hide other views
    document.querySelector('#load_page').style.display = 'none';
    document.querySelector('#profile').style.display = 'block';

}

function submit() {
    document.querySelector('#new_post_form').onsubmit = () => 
    {
        // Select button and content
        const body = document.querySelector('#new_post_text');

        fetch('/create_post', 
        {
            method: 'POST',
            body: JSON.stringify
            ({
                body: body.value
            })
        })
        .then(response => response.json())
        .then(result => 
        {
            // Print result
            console.log(result);
            location.reload()
        })
        return false;
    }
}

