<script lang="ts">
    export let items = [] as any[];
    let showAll = items.length <= 10;

    $: partialList = items.slice(0, 10);
</script>

<div>
    <ul class="overflow-y-auto max-h-72">
        {#if showAll}
            {#each items as item}
                <li>
                    <slot {item} />
                </li>
            {/each}
        {:else}
            {#each partialList as item}
                <li>
                    <slot {item} />
                </li>
            {/each}
        {/if}
    </ul>
    
    {#if !showAll}
        <button class="text-small underline mt-4 hover:opacity-75" on:click={() => showAll = true}>Show all</button>
    {/if}
</div>
