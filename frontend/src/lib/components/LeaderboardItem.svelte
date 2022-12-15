<script>
  export let emoji;
  export let iconUrl;
  export let position;
  export let uses;
</script>

<tr
  class="flex flex-row items-center space-x-3 px-3 py-2 rounded-lg bg-gray-700 font-mono animate-fin"
>
  <td>
    <h4 class="text-2xl font-semibold">{position}.</h4>
  </td>

  <td>
    <img class="mb-1 max-h-10 w-10" src={iconUrl} alt={emoji} />
  </td>

  <td>
    <span class="px-2 py-1 bg-gray-800 rounded-md text-gray-300">{emoji}</span>
  </td>

  <td class="!ml-auto">
    <span>({uses} {uses !== 1 ? 'uses' : 'use'})</span>
  </td>
</tr>
