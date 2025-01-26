<script lang="ts">
    export let bindValue: string = ''; // Declare type explicitly as 'string'
</script>

<div>
    <input
        type="text"
        bind:value={bindValue}
        class="border border-gray-300 p-2 rounded-lg w-full"
        placeholder="Enter value"
    />
</div>
