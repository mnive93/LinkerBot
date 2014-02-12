    $(document).ready(function() {
    var pc = $('.post-container').find('.post-content');

    pc.each( function() {
        var post_data = this.innerHTML;
        var splitted = post_data.split(' ');
        
        for(i=0;i<splitted.length;i++){
            regex = splitted[i].match(/\w+/);
            if(splitted[i][0] == '#' && !splitted[i].match(/\d+/)) {
                regex_len = regex[0].length;
                converted = "<a href='/interest/" + regex[0] + "/'>#" + regex[0] + "</a>" + splitted[i].substring(regex_len+1,splitted[i].length);
                post_data = post_data.replace(splitted[i],converted);
            }
            this.innerHTML = post_data;
        }
    })
});
