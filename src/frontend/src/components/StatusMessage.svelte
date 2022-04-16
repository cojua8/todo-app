<script>
    export let message;
    export let type;

    const colors = { ERROR: "text-red-500", SUCCESS: "text-green-500" };

    $: textColor = colors[type];
</script>

<p class="text-xs italic {textColor}">
    {#if message}
        {message}
    {/if}
</p>
