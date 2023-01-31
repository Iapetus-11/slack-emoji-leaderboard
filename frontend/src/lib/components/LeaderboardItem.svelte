<script>
  export let names;
  export let iconUrl;
  export let position;
  export let uses;
</script>

<tr
  class="flex flex-row items-center space-x-3 px-3 py-2 rounded-lg bg-gray-700 font-mono animate-fin text-sm md:text-base"
>
  <td>
    <h4 class="text-xl md:text-2xl font-semibold">{position}.</h4>
  </td>

  <td>
    <img class="mb-1 min-w-[1.5rem] max-h-10 w-10" src={iconUrl} alt={names.join(', ')} />
  </td>

  <td class="flex flex-row space-x-1.5 whitespace-nowrap truncate">
    {#each names as name}
      <span class="px-2 py-1 bg-gray-800 rounded-md text-gray-300">{name}</span>
    {/each}
  </td>

  <td class="!ml-auto whitespace-nowrap">
    <span>({uses} {uses !== 1 ? 'uses' : 'use'})</span>
  </td>
</tr>
