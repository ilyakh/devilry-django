// vim: set ts=2 sts=2 et sw=2:



(function($){
    $.filtertable = {
      refresh_actions: function(store, actions, targetbox, requires_selection) {
        targetbox.empty();
        $.each(actions, function(i, action) {
            var box = $("<li></li>").appendTo(targetbox);
            var button = $("<a></a>")
              .html(action.label)
              .attr("href", "#")
              .appendTo(box);
            $.each(action.cssclasses, function(ci, cssclass) {
                button.addClass(cssclass);
              });
            button.click(function() {
                var c = $("#" + store.id + " input:checkbox:checked");
                if(c.length == 0 && requires_selection) {
                  store.noselection_dialog.dialog("open");
                  return false;
                }
                store.form.attr("action", action.url);
                store.form.submit();
              });
          });
      },

      create_header: function(store, has_selactions, columns, use_rowactions,
          order_by, order_asc) {
        var thead = $("<thead></thead>")
          .addClass("ui-widget-header");
        var tr = $("<tr></tr>").appendTo(thead);
        if(has_selactions) {
          var th = $("<th></th>")
            .addClass("filtertable-checkboxcell")
            .addClass("ui-state-default")
            .appendTo(tr);
          var checkall = $("<input/>")
            .attr("type", "checkbox")
            .appendTo(th);
          checkall.click(function() {
              var qry ="#" + store.id + " input:checkbox";
              var checked = checkall.is(":checked");
              $(qry).attr("checked", checked);
            });
        }
        $.each(columns, function(i, col) {
            var th = $("<th></th>")
              .addClass("ui-state-default")
              .html(col.title)
              .appendTo(tr);
            if(col.can_order) {
              var icon = $("<span></span>")
                .addClass("ui-icon")
                .addClass("devilry-th-ui-icon")
                .appendTo(th);

              th.addClass("devilry-th-clickable")
              if(order_by == i) {
                icon.addClass(order_asc?"ui-icon-triangle-1-n":"ui-icon-triangle-1-s")
                th.addClass("ui-state-active");
              } else {
                icon.addClass("ui-icon-carat-2-n-s");
              }
              th.click(function() {
                  $.filtertable.refresh(store, {order_by:i});
                  return false;
                });
            }
          });
        if(use_rowactions) {
          var th = $("<th></th>")
            .addClass("ui-state-default")
            .html("&nbsp;")
            .appendTo(tr);
        }
        return thead;
      },

      create_body: function(data, has_selactions, id) {
        var name = id + "-checkbox";
        var tbody = $("<tbody></tbody>")
        $.each(data, function(i, row) {
            var tr = $("<tr></tr>")
              .addClass(i%2?"even":"odd")
              .appendTo(tbody);
            if(has_selactions) {
              var td = $("<td></td>")
                .addClass("filtertable-checkboxcell")
                .appendTo(tr);
              var checkbox = $("<input/>")
                .attr("type", "checkbox")
                .attr("name", name)
                .attr("value", row.id)
                .appendTo(td);
            }
            $.each(row.cells, function(index, cell) {
                var td = $("<td></td>")
                  .html(cell.value)
                  .appendTo(tr);
                if (cell.cssclass) {
                  td.addClass(cell.cssclass);
                };
              });
            if(row.actions.length > 0) {
                var td = $("<td></td>").appendTo(tr);
                $.each(row.actions, function(i, action) {
                    $("<a></a>")
                      .html(action.label)
                      .attr("href", action.url)
                      .button()
                      .appendTo(td);
                  });
            };
          });
        return tbody;
      },

      refresh_table: function(store, json) {
        store.result_table.empty();
        var has_selactions = json.selectionactions.length > 0;
        var thead = $.filtertable.create_header(store, has_selactions,
          json.columns, json.use_rowactions, json.order_by, json.order_asc);
        thead.appendTo(store.result_table);
        var tbody = $.filtertable.create_body(json.data, has_selactions, store.id);
        tbody.appendTo(store.result_table);
      },

      refresh_filters: function(store, filterview) {
        store.filterbox.empty();
        $.each(filterview, function(filterindex, filter) {
            var box = $("<div></div>").appendTo(store.filterbox);
            $("<h4></h4>").html(filter.title).appendTo(box);
            var ul = $("<ul></ul>").appendTo(box);
            var idprefix = store.id + "-filter-" + filterindex + "-";
            $.each(filter.labels, function(i, label) {
                var id = idprefix + i;
                var li = $("<li></li>").appendTo(ul);
                var button = $("<input></input>")
                  .attr("type", "radio")
                  .attr("id", id)
                  .appendTo(li);
                if (label.selected) {
                  button.attr("checked", "checked");
                };
                var label = $("<a></a>")
                  .attr("href", "#")
                  .html(label.label)
                  .appendTo(li);
                label.click(function() {
                    button.click();
                    return false;
                  });
                button.click(function() {
                    var opt = {};
                    opt["filter_selected_"+filterindex] = i;
                    $.filtertable.refresh(store, opt);
                  });
              });
          });
      },


      refresh_pagechanger: function(store, filteredsize, currentpage, perpage) {
        store.pagechangerbox.empty();
        var pages = parseInt("" + filteredsize / perpage) + 1;
        if(filteredsize % perpage == 0) {
          pages --;
        }
        var pagelabel = $("<div></div>")
          .addClass("filtertable-pagelabel")
          .html("Page " + (currentpage+1) + " of " + pages);
        var slider = $("<div></div>");
        pagelabel.appendTo(store.pagechangerbox);
        slider.appendTo(store.pagechangerbox);
        slider.slider({
            max: pages - 1,
            value: currentpage,
            slide: function(e, ui) {
              pagelabel.html("Page " + (ui.value+1) + " of " + pages);
            },
            change: function(e, ui) {
              $.filtertable.refresh(store, {gotopage:ui.value});
            }
        });
      },

      refresh: function(store, options) {
        $.getJSON(store.jsonurl, options, function(json) {
            $.filtertable.refresh_filters(store, json.filterview);
            $.filtertable.refresh_actions(store,
              json.selectionactions, store.selectionactionsbox,
              true);
            $.filtertable.refresh_actions(store,
              json.relatedactions, store.relatedactionsbox);
            $.filtertable.refresh_table(store, json);
            $.filtertable.refresh_pagechanger(store, json.filteredsize,
              json.currentpage, json.perpage);
            store.searchfield.val(json.search);
            //store.sidebar.accordion("option", "autoHeight", true);
            store.sidebar.accordion("resize");
            store.statusmsgbox.html(json.statusmsg);
          });
      }
    };

    $.fn.filtertable = function(jsonurl) {
      return this.each(function() {
          var id = $(this).attr("id");
          var store = {};
          store.id = id;
          store.jsonurl = jsonurl;
          store.form = $("#" + id + " form").first();
          store.searchbox = $("#" + id + " .filtertable-searchbox").first();
          store.selectionactionsbox = $("#" + id + " .filtertable-selectionactions").first();
          store.relatedactionsbox = $("#" + id + " .filtertable-relatedactions").first();
          store.filterbox = $("#" + id + " .filtertable-filters").first();
          store.result_table = $("#" + id + " .filtertable-table").first();
          store.pagechangerbox = $("#" + id + " .filtertable-pagechanger").first();
          store.searchfield = $("#" + id + " .filtertable-searchbox input").first();
          store.statusmsgbox = $("#" + id + " .filtertable-statusmsg").first();

          // Show this dialog when selecting a action when no rows are
          // selected.
          store.noselection_dialog = $("#" + id + " .filtertable-noselection-dialog").first();
          store.noselection_dialog.dialog({
              modal: true,
              autoOpen: false,
              buttons: {
                "Ok": function() {
                  $( this ).dialog( "close" );
                }
              },
            });

          store.sidebar = $("#" + id + "-filtertable-sidebar");
          store.sidebar.accordion({
            header: "h3",
            autoHeight: false,
            event: "mouseover"
          });


          $.filtertable.refresh(store);

          store.searchfield.keydown(function(e) {
              if (e.keyCode==13) {
                $.filtertable.refresh(store, {search:store.searchfield.val()});
                return false;
              }
            });
        });

    };

    $.log = function(message) {
      if(window.console) {
        console.debug(message);
      } else {
        alert(message);
      }
    };
  })(jQuery);
