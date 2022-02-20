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
$("#settings_form").on("submit", () => {
    sessionStorage.setItem("settingsSideBar", true)
})