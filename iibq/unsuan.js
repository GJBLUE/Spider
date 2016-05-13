function unsuan(s) {
    var a = "jmmh.net|iibq.com";
    var c = location.hostname.toLowerCase(); 
    b = false;
    for (i = 0; i < a.split("|").length; i++) {
        if (c.indexOf(a.split("|")[i]) > -1) {
            b = true;
            break
        }
    }
    if (!b) return "";
    var x = s.substring(s.length - 1);
    var d = "abcdefghijklmnopqrstuvwxyz".indexOf(x) + 1;
    var e = s.substring(s.length - d - 12, s.length - d - 1);
    s = s.substring(0, s.length - d - 12);
    var k = e.substring(0, e.length - 1);
    var f = e.substring(e.length - 1);
    for (i = 0; i < k.length; i++) {
        eval("s=s.replace(/" + k.substring(i, i + 1) + "/g,'" + i + "')")
    }
    var g = s.split(f);
    s = "";
    for (i = 0; i < g.length; i++) {
        s += String.fromCharCode(g[i])
    }
    return s
}