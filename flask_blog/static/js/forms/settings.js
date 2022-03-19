//Open and close user's setting sidebar
$("#settings_btn").on("click", () => {
    $("#settings_sidebar").fadeIn("slow")
})
$("#settings_sidebar_btn").on("click", () => {
    $("#settings_sidebar").fadeOut("slow")
})

//Keep settings sidebar open after form submition
if(sessionStorage.getItem("settingsSideBar")) {
    $("#settings_sidebar").toggleClass("hidden")
    sessionStorage.removeItem("settingsSideBar")
}
$("#settings_form").on("submit", (e) => {
    
    // Validate profile pic
    var file = $('#profile_pic').get(0).files[0];
    var size = file.size;
    let max = 2 * 1024 * 1024
    if(size >= max) {
        e.preventDefault()
        $("label[for='profile_pic']").removeClass("form-label")
        $("label[for='profile_pic']").addClass("form-invalid-label")
        $("#profile_pic").removeClass()
        $("#profile_pic").after(`<p class="form-error-message max-w-full"><span class="font-medium">Oops! File too large. Max 2MB</p>`)
        $("#profile_pic").addClass("block w-full text-sm text-red-900 bg-red-50 rounded-lg border border-red-300 cursor-pointer dark:text-red-400 focus:outline-none focus:border-transparent dark:bg-red-700 dark:border-red-600 dark:placeholder-red-400")
        $("#settings_sidebar").scrollTop(0)
    }
    sessionStorage.setItem("settingsSideBar", true)
})