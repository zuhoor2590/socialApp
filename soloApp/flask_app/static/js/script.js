$(document).ready(function() {
    //jquery for registerForm
    $("#registerForm").submit(function(e) {
        e.preventDefault();  // Prevent default form submission

        $.ajax({
            type: "POST",
            url: "/register",
            data: $(this).serialize(),
            dataType: "json",
            success: function(response) {
                $("#flashMessages").html("");  // Clear previous messages

                if (!response.success) {
                    response.messages.forEach(msg => {
                        $("#flashMessages").append(`<div class="alert alert-danger">${msg}</div>`);
                    });
                } else {
                    $("#flashMessages").append(`<div class="alert alert-success">${response.messages[0]}</div>`);
                    setTimeout(() => window.location.href = "/posts", 1000);  // Redirect after 1s
                }
            }
        });
    });
    //jquery for login form
    $("#loginForm").submit(function(e)
    {
        e.preventDefault();

        $.ajax
        ({
            type: "POST",
            url: "/login",
            data: $(this).serialize(),
            dataType: "json",
            success: function(response) 
            {
                $("#flashMessages").html("");

                if (!response.success) {
                    response.messages.forEach(msg => {
                        $("#flashMessages").append(`<div class="alert alert-danger">${msg}</div>`);
                    });
                } else {
                    window.location.href = response.redirect_url;  // Redirect on success
                }
            }
        });
    });

    //jquery for new post form
    $("#newPost").submit(function(e) {
        e.preventDefault(); // Prevent form from submitting normally

        $.ajax({
            type: "POST",
            url: "/posts/create",
            data: $(this).serialize(),
            dataType: "json",
            success: function(response) {
                $("#flashMessages").html("");  // Clear previous messages

                if (!response.success) {
                    response.messages.forEach(msg => {
                        $("#flashMessages").append(`<div class="alert alert-danger">${msg}</div>`);
                    });
                } else {
                    $("#flashMessages").append(`<div class="alert alert-success">${response.messages[0]}</div>`);
                    setTimeout(() => window.location.href = "/posts", 1000);  // Redirect after 1s
                }
            }
        });
    });
    
    //jquery ajax for comment on post form
    $("#commentForm").submit(function(e) {
        e.preventDefault(); // Prevent form from submitting normally

        $.ajax({
            type: "POST",
            url: `/posts/${$("#comment_post").val()}/comments/create`, // Dynamic post ID Get post ID from hidden input #comment_post.val() is the Current_post id
            data: $(this).serialize(),
            dataType: "json",
            success: function(response) {
                $("#flashMessages").html("");  // Clear previous messages

                if (!response.success) {
                    response.messages.forEach(msg => {
                        $("#flashMessages").append(`<div class="alert alert-danger">${msg}</div>`);
                    });
                } else {
                    $("#flashMessages").append(`<div class="alert alert-success">${response.messages[0]}</div>`);
                    setTimeout(() => location.reload(), 1000);  // Redirect after 1s
                }
            }
        });
    });

    //jquery ajax for update form   
    $("#updatePost").submit(function(e) {
        e.preventDefault(); // Prevent form from submitting normally

        $.ajax({
            type: "POST",
            url: `/posts/${$("#post_id").val()}/update`, // Dynamic post ID Get post ID from hidden input #post_id.val() is the Current_post id
            data: $(this).serialize(),
            dataType: "json",
            success: function(response) {
                $("#flashMessages").html("");  // Clear previous messages

                if (!response.success) {
                    response.messages.forEach(msg => {
                        $("#flashMessages").append(`<div class="alert alert-danger">${msg}</div>`);
                    });
                } else {
                    $("#flashMessages").append(`<div class="alert alert-success">${response.messages[0]}</div>`);
                    setTimeout(() => window.location.href = "/posts", 1000);  // Redirect after 1s
                }
            }
        });
    });
});































































    // $("#commentForm").submit(function (e) {
    //     e.preventDefault(); // Prevent form from submitting normally
    
    //     $.ajax({
    //         type: "POST",
    //         url: `/posts/${$("#comment_post").val()}/comments/create`, // Dynamic post ID
    //         data: $(this).serialize(),
    //         dataType: "json",
    //         success: function (response) {
    //             $("#flashMessages").html(""); // Clear previous messages
    
    //             if (!response.success) {
    //                 response.messages.forEach(msg => {
    //                     $("#flashMessages").append(`<div class="alert alert-danger">${msg}</div>`);
    //                 });
    //             } else {
    //                 $("#flashMessages").append(`<div class="alert alert-success">${response.messages[0]}</div>`);
    //                 // Clear the input field
    //                 $("#comment").val("");
    
    //                 // Auto-hide success message after 2 seconds
    //                 setTimeout(() => {
    //                     $(".alert-success").fadeOut("slow");
    //                 }, 2000);

    //             }
    //         }
    //     });
    // });
    