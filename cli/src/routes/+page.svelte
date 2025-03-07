<!-- <h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p> -->

<script lang="ts">
    // Это компонент на TypeScript
    interface ConnectionStatus {
      http: boolean;
      websocket: boolean
    }

    interface ConnectionAddresses {
      http: string;
      websocket: string;
    }

    let connections: ConnectionStatus = {
      http: true,
      websocket: true
    }

    let connection_addresses: ConnectionAddresses = {
      http: "http://localhost:8000/",
      websocket: "ws://localhost:8000/ws"
    }

    async function checkConnection(type: keyof ConnectionAddresses): Promise<boolean> {
      try {
        if (type === 'http') {
          const response = await fetch(connection_addresses.http);
          return response.ok;
        } else {
          return new Promise((resolve) => {
            const ws = new WebSocket(connection_addresses.websocket);

            ws.onopen = () => {
              ws.close();
              resolve(true);
            };

            ws.onerror = () => {
              resolve(false);
            };

            setTimeout(() => {
              ws.close();
              resolve(false);
            }, 5000);
          });
        }
      } catch (error) {
        console.log(`Ошибка при проверке ${type} полкдючения:`, error);
        return false;
      }
    } 

    function toggleConnection(type: keyof ConnectionStatus) {
      connections = {
        ...connections,
        [type]: !connections[type]
      };
    }

    let address = "ws://localhost/ws"

    let paragraphs = [
        "Это первый параграф с примером текста. Здесь может быть любая информация.",
        "А это второй параграф, который демонстрирует структуру страницы.",
        "Третий параграф дополняет контент и показывает визуальное разделение."
    ];
</script>

<!-- Основной котейнер беженый -->
 <div class="min-h-screen bg-[#F5E6D3]">
    <!-- Центральный контейнер -->
      <div class="container mx-auto px-4 py-8 bg-[#FAF3E0] rounded-lg shadow-sm">
        <div class="container mb-10 bg-[RED]">
          <h1>Hello world</h1>
        </div>
        {#each paragraphs as paragraph}
          <!-- Блоки параграфа -->
          <div class="mb-8 last:mb-0">
            <p class="text-gray-800 leading-relaxed">
              {paragraph}
            </p>
          </div>
        {/each}
      </div>
      <div class="container mx-auto mt-4 px-4 py-8 bg-[#FAF3E0] rounded-lg shadow-sm items-center justify-center">
        <!-- Индикатор HTTP -->
        <div class="flex items-center justify-between">
          <span class="font-medium">HTTP:</span>
          <div 
              class={`
                  w-8 h-8 rounded-full cursor-pointer transition-colors duration-300
                  ${connections.http ? 'bg-green-500 hover:bg-green-600' : 'bg-red-500 hover:bg-red-600'}
              `}
              on:click={() => toggleConnection('http')}
            />
        </div>

        <!-- Индикатор WebSocket -->
        <div class="flex items-center justify-between mt-2">
            <span class="font-medium">WebSocket:</span>
            <div 
                class={`
                    w-8 h-8 rounded-full cursor-pointer transition-colors duration-300
                    ${connections.websocket ? 'bg-blue-500 hover:bg-blue-600' : 'bg-red-500 hover:bg-red-600'}
                `}
                on:click={() => toggleConnection('websocket')}
            />
        </div>
      </div>

      <div class="flex items-center justify-center mt-2">
        <!-- Using utilities: -->
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        on:click={() => checkConnection('http').then(result => console.log('HTTP подключение:', result))}>
          <span>Проверить HTTP</span>
        </button>

        <button
          class="m-2 bg-[grey]"
          on:click={() => checkConnection('http').then(result => console.log('HTTP подключение:', result))}>
          Проверить HTTP
        </button>
        
        <button class="m-2 bg-[grey]"
          on:click={() => checkConnection('websocket').then(result => console.log('WebSocket подключение:', result))} >
          Проверить WebSocket
        </button>
      </div>
   
 </div>
