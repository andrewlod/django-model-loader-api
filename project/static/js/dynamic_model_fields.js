(function($) {
    $(function() {
        var outputTypeField = $('#id_model_output_type'),
            labelMap = $('#id_model_label_map').parent().parent();

        function toggleLabelMap(value) {
            value == 'String' ? labelMap.show() : labelMap.hide();
        }

        toggleLabelMap(outputTypeField.val());

        outputTypeField.change(function() {
            toggleLabelMap($(this).val());
        });
    });
})(jQuery);