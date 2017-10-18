import Cookies from 'js-cookie'

/// #if !PRODUCTION
Cookies.defaults['secure'] = false
Cookies.defaults['domain'] = 'localhost'
Cookies.defaults['expires'] = ''
/// #else
Cookies.defaults['secure'] = true
Cookies.defaults['domain'] = 'anna.elde.codes'
Cookies.defaults['expires'] = 365
/// #endif

export default Cookies

export var cookie =
    Cookies.getJSON('session') != undefined ? Cookies.getJSON('session') : {}

export function setCookie(key, value) {
    cookie[key] = value
    Cookies.set('session', cookie)
}
