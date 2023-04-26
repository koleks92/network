const currentRoute = window.location.pathname;
if (currentRoute === '/')
    {
    document.addEventListener('DOMContentLoaded', function() {
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
    }); 
    }
else if (currentRoute.startsWith('/profile'))
    {
        const user_name = currentRoute.split('/').pop();
        fetch(`/follow_unfollow/${user_name}`, {
            method: "GET",
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            // Update the UI to reflect the new follow status
            const followButton = document.getElementById('follow_button');
            const button = document.createElement('button');
            if (data.message === "Followed") {
                button.innerText = 'Unfollow';
            } else {
                button.innerText = 'Follow';
            }
            button.addEventListener('click', function()
            { 
                fetch(`/follow_unfollow/${user_name}`, {
                    method: "PUT",
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data.message);
                    // Update the UI to reflect the new follow status + Add 1 or Remove 1 from user_followers number
                    if (data.message === "Followed") {
                        button.innerText = 'Unfollow';
                        let numberOfFollowers = document.getElementById("user_followers")
                        let intNumberOfFollowers = parseInt(numberOfFollowers.innerHTML);
                        numberOfFollowers.innerHTML = intNumberOfFollowers + 1;
                    } else {
                        button.innerText = 'Follow';
                        let numberOfFollowers = document.getElementById("user_followers")
                        let intNumberOfFollowers = parseInt(numberOfFollowers.innerHTML);
                        numberOfFollowers.innerHTML = intNumberOfFollowers - 1;
                    }
                });
            });
            followButton.append(button)
        })
    }