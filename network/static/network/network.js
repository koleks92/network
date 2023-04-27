const currentRoute = window.location.pathname;
if (currentRoute === '/')
    { // Creating new post
        document.addEventListener('DOMContentLoaded', function() 
        {
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
            edits()
        }); 
    }
else if (currentRoute.startsWith('/profile'))
    { 
        document.addEventListener('DOMContentLoaded', function() 
        {
            edits();
        });
        
        // Follow/Unfollow
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
    
function edits()
{

    // Get all edit buttons
    const editButtons = document.querySelectorAll('.edit_button');

    // Add a click event listener to each edit button
    editButtons.forEach(function(editButton) {
        editButton.addEventListener('click', function(event) 
        {
            // Get the parent element of the clicked button
            const postDiv = event.target.parentNode;
            
            // Get body and edit button and post_id from button
            const body = postDiv.querySelector('.post_body');
            const button = postDiv.querySelector('.edit_button');
            const post_id  = button.value;

            // Create textarea for edit
            const edit = document.createElement("textarea");
            edit.classList.add("edit_textarea");
            edit.innerHTML = body.innerHTML;
            postDiv.replaceChild(edit, body);

            // Create button to save 
            const save = document.createElement("button");
            save.innerText = "Save";
            // Add eventlistener and post via edit view 
            save.addEventListener('click', function() 
            {
                edit_text = postDiv.querySelector(".edit_textarea").value;
                fetch(`/edit/${post_id}`, {
                    method: "POST",
                    body: JSON.stringify
                    ({
                        body: edit_text
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data.message);
                    postDiv.replaceChild(button, save);
                    body.innerHTML = edit_text;
                    postDiv.replaceChild(body, edit);

                })
            })
            postDiv.replaceChild(save, button);
        });
    }); 
}