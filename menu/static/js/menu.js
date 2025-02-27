const autoCollapseMenus = (event) => {
    // find parent navbar element
    const navbar = event.target.closest('nav.navbar');
    console.log(event.target, navbar, navbarToggler);
    // check if the clicked element is a dropdown toggle or a submenu item
    if (event.target.matches('li.submenu>a.dropdown-item.dropdown-toggle')) {
        // for nested submenus, prevent parent dropdown menu from collapsing on click
        event.stopPropagation();
        // get the target submenu (the ul.dropdown-menu sibling of the clicked item)
        targetSubmenu = event.target.parentElement.querySelector('ul.dropdown-menu');
        // find any open submenu items
        // set class and aria attributes to closed unless element is clicked element or direct ancestor
        if (targetSubmenu) {
            navbar.querySelectorAll('li.submenu>ul.dropdown-menu.show').forEach((subMenu) => {
                if (!subMenu.contains(targetSubmenu)) {
                    // dropdown toggle link - remove 'show' class, set aria-expanded to fale
                    subMenu.classList.remove('show');
                    // Get the sibling ul.dropdown-menu
                    const dropDownToggle = subMenu.parentElement.querySelector('a[aria-expanded="true"].dropdown-item.dropdown-toggle');
                    if (dropDownToggle) {
                        // Remove the 'show' class
                        dropDownToggle.classList.remove('show');
                        dropDownToggle.setAttribute('aria-expanded', 'false');
                    }
                }
            });
        };
    }
};

const handleDropdownShow = (event) => {
    // Check if the clicked item is a sticky menu (or child of), and if the "mobile" menu is expanded 
    // (by examining the aria-expanded attribute of the toggle button). 
    // If so, raise the click event for the toggler button which causes the mobile menu to collapse.
    const navbar = event.target.closest('nav.navbar');
    const navbarToggler = navbar.querySelector("button.navbar-toggler");
    if (navbarToggler.getAttribute("aria-expanded") === "true" && 
        event.target.closest('div.sticky li.nav-item.dropdown') && 
        navbarToggler) {
        navbarToggler.click();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('nav.navbar').forEach((navbar) => {
        navbar.addEventListener('click', autoCollapseMenus);
        navbar.addEventListener("show.bs.dropdown", handleDropdownShow);
    })
});