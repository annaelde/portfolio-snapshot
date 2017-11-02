/**
 *  Anna Elde
 *  August 12, 2017
 *  Barba.Js Initialization Script
 */
'use strict'
import Barba from 'barba.js'
import { default as Cookies, cookie, setCookie } from './cookies.js'
import { isIE } from './detectIE.js'
import { Loader } from './loader.js'
import { ToggleBox } from './toggleBox.js'
import ScrollReveal from 'scrollreveal'

/**
 *  Blog Post Detail View 
 */
var post_detail = Barba.BaseView.extend({
    namespace: 'post_detail',
    tocScroll: null,
    onEnter: function() {},
    onEnterCompleted: function() {
        // Add comment button to open Disqus
        var button = document.getElementById('show-comments')
        button.addEventListener('click', function() {
            var frame = document.getElementById('disqus_thread')
            frame.src = '/static/disqus.html'
            this.style.display = 'none'
        })

        // Add table of contents sidebar, if there is a TOC
        var toc = document.querySelector('.toc')
        // Make sure it's not disabled
        var disable = document.querySelector('.toc--disabled')
        if (toc && !disable) {
            var content = document.querySelector('.post__content')
            var minScroll, maxScroll
            var sidebar = toc.cloneNode(true)
            var calculateBounds = () => {
                if (isIE) {
                    minScroll = parseInt(toc.offsetHeight) + parseInt(toc.offsetTop)
                    maxScroll = parseInt(content.offsetHeight) + parseInt(content.offsetTop) - parseInt(toc.offsetTop)
                } else {
                    minScroll = Number.parseInt(toc.offsetHeight) + Number.parseInt(toc.offsetTop)
                    maxScroll = Number.parseInt(content.offsetHeight) + Number.parseInt(content.offsetTop) - Number.parseInt(toc.offsetTop)
                }
            }

            sidebar.className += ' sidebar'
            document.querySelector('.post__content').appendChild(sidebar)

            this.tocScroll = () => {
                calculateBounds()
                if (window.pageYOffset > minScroll && window.pageYOffset < maxScroll && sidebar.className.indexOf('sidebar--active') === -1) {
                    sidebar.className += ' sidebar--active'
                } else if (window.pageYOffset < minScroll || window.pageYOffset > maxScroll) {
                    sidebar.className = sidebar.className.replace(' sidebar--active', '')
                }
            }

            this.tocScroll()
            window.addEventListener('scroll', this.tocScroll)
        }
    },
    onLeave: function() {
        window.removeEventListener('scroll', this.tocScroll)
    },
    onLeaveCompleted: function() {}
})

/**
 *  Blog Post List View 
 * @property {string} namespace         Data-namespace attribute identifying this view
 * @property {boolean} tagCloudOpen     Whether tag menu is open
 */
var post_list = Barba.BaseView.extend({
    namespace: 'post_list',
    tagCloudOpen: true,
    loader: Object.create(Loader),
    onEnter: function() {
        window.sr = ScrollReveal()
    },
    onEnterCompleted: function() {
        // Fix post list flex styles for IE
        if (isIE) {
            let list = document.getElementsByClassName('post-list--vert')[0]
            list.className += ' post-list--vert--ie'
        }

        // Load Disqus
        this.loader.load('//aecodes.disqus.com/count.js', 'dsq-count-scr')

        // Instantiate tag cloud
        var tagCloud = Object.create(ToggleBox)
        tagCloud['id'] = 'tag-cloud'
        tagCloud['wrapper'] = document.getElementById('tag-cloud')
        tagCloud['button'] = document.querySelector('#tag-cloud .toggle')
        tagCloud['toggle'] = document.querySelector('#tag-cloud .toggle__switch')
        tagCloud['inner'] = document.querySelector('#tag-cloud .tag-list')
        tagCloud.init()

        sr.reveal('.post-list__item')
    },
    onLeave: function() {
        this.loader.cleanup('DISQUSWIDGETS')
        window.sr = undefined
    },
    onLeaveCompleted: function() {}
})

/**
 *  Portfolio List View
 */
var project_list = Barba.BaseView.extend({
    namespace: 'project_list',
    filters: {},
    menuOpen: false,
    clickOut: null,
    onEnter: function() {
        window.sr = ScrollReveal()
    },
    onEnterCompleted: function() {
        var filterButton = document.querySelector('.filter__button')
        var filterOptions = document.querySelector('.filter .filter__options')
        var activeFilter = false
        var projectList = document.getElementsByClassName('project-list--vert')[0]

        var closeMenu = () => {
            filterButton.className = filterButton.className.replace(' filter__button--opened', '')
            if (filterOptions.className.indexOf(' filter__options--closed') == -1) filterOptions.className += ' filter__options--closed'
            this.menuOpen = false
        }

        var openMenu = () => {
            if (filterButton.className.indexOf(' filter__button--opened') == -1) filterButton.className += ' filter__button--opened'
            filterOptions.className = filterOptions.className.replace(' filter__options--closed', '')
            this.menuOpen = true
        }

        this.clickOut = event => {
            if (!event) return
            var clickOut = !filterOptions.contains(event.target) && !filterButton.contains(event.target)
            if (clickOut && this.menuOpen) closeMenu()
        }

        document.addEventListener('click', this.clickOut)

        filterButton.addEventListener('click', () => {
            if (this.menuOpen) closeMenu()
            else openMenu()
        })

        // Init all the filter options, styles, and links
        var options = filterOptions.getElementsByClassName('filter__option')
        for (let i = 0; i < options.length; i++) {
            // Get the slug
            let start = options[i].href.lastIndexOf('=')
            let slug = options[i].href.substring(start + 1, options[i].href.length)
            let name = options[i].innerHTML

            // Init the filters object
            this.filters[name] = {
                slug: slug,
                active: false
            }

            // Determine whether the URL contains the slug
            let value = window.location.search.indexOf(slug)

            // Set filter option to 'active' if the URL contains the slug
            if (value > -1) {
                activeFilter = true
                this.filters[name].active = true

                // Remove inactive class, add active class
                options[i].className = options[i].className.replace(' filter__option--inactive', '')
                if (options[i].className.indexOf(' filter__option--active') == -1) options[i].className += ' filter__option--active'

                // Remove the last URL query
                let href = options[i].href
                let start = href.lastIndexOf('&')
                if (start > -1) {
                    let remove = href.substring(start, href.length)
                    href = href.replace(remove, '')
                }

                // Remove any other instances of the URL parameter
                // because clicking this is supposed to 'deactivate' the filter
                href = href.replace('&tag=' + slug, '')
                href = href.replace('?tag=' + slug, '')
                href = href.replace('/&tag=', '/?tag=')
                options[i].href = href
            } else {
                // Style filter if it's inactive
                this.filters[name].active = false
                options[i].className = options[i].className.replace(' filter__option--active', '')
                if (options[i].className.indexOf(' filter__option--inactive') == -1) options[i].className += ' filter__option--inactive'
            }

            // Add event handler for AJAX behavior
            options[i].addEventListener('click', e => {
                e.preventDefault()
                var header = {
                    'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                }

                var request = require('superagent')
                request
                    .get(options[i].href)
                    .set(header)
                    .end((error, response) => {
                        if (error || !response.ok) return

                        // Swap the filter's state, since it was clicked
                        this.filters[name].active = this.filters[name].active ? false : true

                        // Add styles to filter
                        if (this.filters[name].active) {
                            // Remove inactive class, add active class
                            options[i].className = options[i].className.replace(' filter__option--inactive', '')
                            if (options[i].className.indexOf(' filter__option--active') == -1) options[i].className += ' filter__option--active'
                        } else {
                            // Remove active class, add inactive
                            options[i].className = options[i].className.replace(' filter__option--active', '')
                            if (options[i].className.indexOf(' filter__option--inactive') == -1) options[i].className += ' filter__option--inactive'
                        }

                        // Update window history
                        let start = options[i].href.indexOf('?')
                        history.pushState(null, null, options[i].href.substring(start, options[i].href.length))

                        // Set active filter to false, since we're going to iterate through the filters to check
                        activeFilter = false

                        // Split URL into root and query
                        var root = window.location.href.replace(window.location.search, '')
                        var query = window.location.search

                        for (let j = 0; j < options.length; j++) {
                            var identity = options[j].innerHTML

                            // Cases for a window with no querystring
                            // If the filter is active, make sure the URL is only the root
                            if (query.indexOf('?tag=') == -1 && this.filters[identity].active) {
                                options[j].href = root
                                activeFilter = true
                            } else if (query.indexOf('?tag=') == -1)
                                // If inactive, add a query string
                                options[j].href = root + '?tag=' + this.filters[identity].slug
                            else if (this.filters[identity].active) {
                                // If the filter is active, make sure to remove the slug from the URL
                                options[j].href = (root + query)
                                    .replace('&tag=' + this.filters[identity].slug, '')
                                    .replace('?tag=' + this.filters[identity].slug, '')
                                    .replace('/&tag=', '/?tag=')
                                activeFilter = true
                            } else
                                // Add slug to end of URL
                                options[j].href = root + query + '&tag=' + this.filters[identity].slug
                        }

                        // Update filter button
                        if (activeFilter) {
                            if (filterButton.className.indexOf(' filter__button--active') == -1) filterButton.className += ' filter__button--active'
                        } else filterButton.className = filterButton.className.replace(' filter__button--active', '')

                        // Update DOM
                        while (projectList.hasChildNodes()) projectList.removeChild(projectList.lastChild)
                        var range = document.createRange()
                        range.selectNode(projectList)
                        projectList.appendChild(range.createContextualFragment(response.text))
                    })
            })
        }

        // Initialize the view
        filterButton.style.display = 'block'

        // Highlight filter button if active/inactive
        if (activeFilter) {
            if (filterButton.className.indexOf(' filter__button--active') == -1) filterButton.className += ' filter__button--active'
        }

        if (this.menuOpen) openMenu()
        else closeMenu()

        setTimeout(() => {
            filterButton.style.transition = ''
            if (!isIE) filterOptions.style.transition = ''
        }, 200)

        sr.reveal('.project-list__item', { origin: 'bottom' })
        if (!this.menuOpen) sr.reveal('.filter', { origin: 'right' })
    },
    onLeave: function() {
        document.removeEventListener('click', this.clickOut)
        window.sr = undefined
    },
    onLeaveCompleted: function() {}
})

/**
 *  Contact Form View 
 */
var contact = Barba.BaseView.extend({
    namespace: 'contact',
    loader: Object.create(Loader),
    onEnter: function() {},
    onEnterCompleted: function() {
        this.loader.load('https://www.google.com/recaptcha/api.js')

        var contact = document.getElementById('contact')
        var loadingIcon = document.getElementsByClassName('contact__loading')[0];
        contact.addEventListener('submit', function(e) {
            loadingIcon.style.display = "block";
            e.preventDefault()
            ajaxSubmit()
        })

        function ajaxSubmit() {
            var status = document.getElementById('status')
            var csrftoken = document.querySelector('[name="csrfmiddlewaretoken"]').value
            var request = new XMLHttpRequest()

            request.onreadystatechange = function() {
                if (request.readyState == 4) {
                    if (request.status == 201) {
                        // Remove the submit button
                        var submit = contact.getElementsByClassName('contact__submit')[0]
                        loadingIcon.style.display = "none";
                        submit.parentNode.removeChild(submit)

                        // Style the status message
                        status.classList.remove('hide')
                        status.classList.add('show')
                        if (status.classList.contains('error')) status.classList.remove('error')
                        status.classList.add('success')

                        // Set the status message
                        status.innerHTML = JSON.parse(request.responseText).response
                    } else {
                        // Set the status message
                        status.innerHTML = JSON.parse(request.responseText).response

                        // Style the status message
                        status.classList.remove('hide')
                        status.classList.add('show')
                        if (!status.classList.contains('error')) status.classList.add('error')
                    }
                }
            }

            request.open('POST', '.')
            request.setRequestHeader('X-CSRFToken', csrftoken)
            request.send(new FormData(contact))
        }
    },
    onLeave: function() {
        this.loader.cleanup('grecaptcha')
    },
    onLeaveCompleted: function() {}
})

/**
 *  Home View
 */
var home = Barba.BaseView.extend({
    namespace: 'home',
    loader: Object.create(Loader),
    onEnter: function() {
        window.sr = ScrollReveal()
    },
    onEnterCompleted: function() {
        this.loader.load('//aecodes.disqus.com/count.js', 'dsq-count-scr')
        sr.reveal('.intro__resume-button')
        sr.reveal('.post-list__item')
    },
    onLeave: function() {
        this.loader.cleanup('DISQUSWIDGETS')
        window.sr = undefined
    },
    onLeaveCompleted: function() {}
})

/*
 *  Init App
 */

home.init()
post_detail.init()
post_list.init()
contact.init()
project_list.init()

Barba.Pjax.start()
Barba.Prefetch.init()

/*
 *  Defining Barba Transitions 
 */
var HideShowTransition = Barba.BaseTransition.extend({
    start: function() {
        this.newContainerLoading.then(this.finish.bind(this))
    },

    finish: function() {
        if (!window.location.hash) {
            document.body.scrollTop = 0
            window.scroll(0, 0)
        }

        this.done()
    }
})

Barba.Pjax.getTransition = function() {
    return HideShowTransition
}
