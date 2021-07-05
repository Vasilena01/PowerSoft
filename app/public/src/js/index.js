// Importing TinyMCE
//import tinymce from 'tinymce/tinymce';
//window.tinymce = tinymce;

// Importing TinyMCE icons
//import 'tinymce/icons/default';

// Importing TinyMCE theme and skins
//import 'tinymce/themes/silver';

// Importing TinyMCE plugins
//import 'tinymce/plugins/link';
//import 'tinymce/plugins/code';
//import 'tinymce/plugins/image';
//import 'tinymce/plugins/media';
//import 'tinymce/plugins/preview';
//import 'tinymce/plugins/anchor';
//import 'tinymce/plugins/fullscreen';
//import 'tinymce/plugins/lists';

// Importing custom js
import './helpers.js';
import './msg.js';

// Event triggered when all of the js has loaded
const on_js_load = new Event('on_js_load');
document.dispatchEvent(on_js_load);

// Importing the scss
import '../scss/main.scss';
