const React = window.React;
const RichUtils = window.DraftJS.RichUtils;

class FontAwesomeSource extends React.Component {
    componentDidMount() {
        const { editorState, entityType, onComplete } = this.props;

        const content = editorState.getCurrentContent();

        const contentWithEntity = content.createEntity(
            entityType.type,
            'MUTABLE',
            {
                fragment: window.getSelection().toString(),
            },
        );
        const selection = editorState.getSelection();
        const entityKey = contentWithEntity.getLastCreatedEntityKey();
        const nextState = RichUtils.toggleLink(
            editorState,
            selection,
            entityKey,
        );

        onComplete(nextState);
    }

    render() {
        return null;
    }
}

const FontAwesome = props => {
    return React.createElement(
        'fontawesome',
        {
            class: 'fa-entity',
        },
        props.children,
    );
};

window.draftail.registerPlugin({
    type: 'FONTAWESOME',
    source: FontAwesomeSource,
    decorator: FontAwesome,
});