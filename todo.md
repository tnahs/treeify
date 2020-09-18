# TODOs

# BUGS

- Extra spaces on a line cause an error. The `.small    :: ProxyImage` Node shouldn't raise an Exception.

``` console
treeify.TreeIndentationError: Input string contains invalid indentation on line 20.
011:             Spacer
012:         .pages :: Pages :: List[PageType]
013:             Lazy
014:             Layout
015:             LazyGallery
016:             LayoutGallery
017:                 .contents List[ContentType]
018:                     Image
019:                         .proxy_images :: ProxyImageManager
020:                             .small    :: ProxyImage
020:                             ^^^^^^^^^^^^^^^^^^^^^^^
(treeify-V1El5evB-py3.8) shant@Shants-MacBook-Pro treeify %
```
