$(document).ready(function(){
  // For each item in .content-markdown
  $(".content-markdown").each(function() {
    // Get the text content from .content-markdown class
    var content = $(this).text()

    // Transform the markdown text content in html content
    var marked_content = marked(content)
    $(this).html(marked_content)
  })

  // Use image responsive on markdown
  $(".content-markdown img").each(function() {
    $(this).addClass("img-responsive");
  })
})
