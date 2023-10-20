var dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.NameLink = function (props) {
    return React.createElement(
        'a',
        { href: '/player/' + props.value.replace(/\s[&\/\\#,+()$~%.'":*?<>{}]/g, '-').toLowerCase() },
        props.value
    );
};