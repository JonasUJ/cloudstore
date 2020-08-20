async function fetchData(url = '', data = {}, method = 'POST') {
    const headers = {
        'X-CSRFToken': get('csrfmiddlewaretoken'),
        'Encoding-Type': 'gzip',
    }

    const request = {
        method: method,
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: headers,
    }

    if (method.toLowerCase() != 'get' && method.toLowerCase() != 'head') {
        let form = new FormData();
        for (const key in data) {
            form.append(key, data[key]);
        }
        request.body = form;
    }

    let response = await fetch(url, request);
    if (response.status < 200 || response.status >= 300) {
        throw response;
    }

    try {
        return await response.json();
    } catch (e) {
        return '';
    }
}

const c = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

function randomString(len) {
    return [...Array(len)].map(_ => c[~~(Math.random() * c.length)]).join('')

}

function copyToClipboard(text) {
    var temp = document.createElement('input');
    temp.classList.add('position', 'fixed');
    document.getElementsByTagName('body')[0].prepend(temp);
    temp.value = text;
    temp.focus();
    temp.select();
    document.execCommand('copy');
    temp.remove();
}

function get(name) {
    return document.getElementsByName(name)[0].value;
}

filetypes = ['3G2','3GA','3GP','7Z','AA','AAC','AC','ACCDB','ACCDT','ADN','AI','AIF','AIFC','AIFF','AIT','AMR','ANI','APK','APP','APPLESCRIPT','ASAX','ASC','ASCX','ASF','ASH','ASHX','ASMX','ASP','ASPX','ASX','AU','AUP','AVI','AXD','AZE','BAK','BASH','BAT','BIN','BLANK','BMP','BOWERRC','BPG','BROWSER','BZ2','C','CAB','CAD','CAF','CAL','CD','CER','CFG','CFM','CFML','CGI','CLASS','CMD','CODEKIT','COFFEE','COFFEELINTIGNORE','COM','COMPILE','CONF','CONFIG','CPP','CPTX','CR2','CRDOWNLOAD','CRT','CRYPT','CS','CSH','CSON','CSPROJ','CSS','CSV','CUE','DAT','DB','DBF','DEB','DGN','DIST','DIZ','DLL','DMG','DNG','DOC','DOCB','DOCM','DOCX','DOT','DOTM','DOTX','DOWNLOAD','DPJ','DS_STORE','DTD','DWG','DXF','EDITORCONFIG','EL','ENC','EOT','EPS','EPUB','ESLINTIGNORE','EXE','F4V','FAX','FB2','FLA','FLAC','FLV','FOLDER','GADGET','GDP','GEM','GIF','GITATTRIBUTES','GITIGNORE','GO','GPG','GZ','H','HANDLEBARS','HBS','HEIC','HS','HSL','HTM','HTML','IBOOKS','ICNS','ICO','ICS','IDX','IFF','IFO','IMAGE','IMG','IN','INDD','INF','INI','ISO','J2','JAR','JAVA','JPE','JPEG','JPG','JS','JSON','JSP','JSX','KEY','KF8','KMK','KSH','KUP','LESS','LEX','LICX','LISP','LIT','LNK','LOCK','LOG','LUA','M','M2V','M3U','M3U8','M4','M4A','M4R','M4V','MAP','MASTER','MC','MD','MDB','MDF','ME','MI','MID','MIDI','MK','MKV','MM','MO','MOBI','MOD','MOV','MP2','MP3','MP4','MPA','MPD','MPE','MPEG','MPG','MPGA','MPP','MPT','MSI','MSU','NEF','NES','NFO','NIX','NPMIGNORE','ODB','ODS','ODT','OGG','OGV','OST','OTF','OTT','OVA','OVF','P12','P7B','PAGES','PART','PCD','PDB','PDF','PEM','PFX','PGP','PH','PHAR','PHP','PKG','PL','PLIST','PM','PNG','PO','POM','POT','POTX','PPS','PPSX','PPT','PPTM','PPTX','PROP','PS','PS1','PSD','PSP','PST','PUB','PY','PYC','QT','RA','RAM','RAR','RAW','RB','RDF','RESX','RETRY','RM','ROM','RPM','RSA','RSS','RTF','RU','RUB','SASS','SCSS','SDF','SED','SH','SITEMAP','SKIN','SLDM','SLDX','SLN','SOL','SQL','SQLITE','STEP','STL','SVG','SWD','SWF','SWIFT','SYS','TAR','TCSH','TEX','TFIGNORE','TGA','TGZ','TIF','TIFF','TMP','TORRENT','TS','TSV','TTF','TWIG','TXT','UDF','VB','VBPROJ','VBS','VCD','VCS','VDI','VDX','VMDK','VOB','VSCODEIGNORE','VSD','VSS','VST','VSX','VTX','WAR','WAV','WBK','WEBINFO','WEBM','WEBP','WMA','WMF','WMV','WOFF','WOFF2','WPS','WSF','XAML','XCF','XLM','XLS','XLSM','XLSX','XLT','XLTM','XLTX','XML','XPI','XPS','XRB','XSD','XSL','XSPF','XZ','YAML','YML','Z','ZIP','ZSH'];
imgtypes = ['JPG', 'JPEG', 'JPE', 'GIF', 'PNG', 'SVG', 'BMP', 'ICO', 'WEBP']
