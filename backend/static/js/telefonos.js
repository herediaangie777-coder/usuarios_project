document.addEventListener('DOMContentLoaded', () => {
    const btnAdd = document.getElementById('add-phone-btn');
    const container = document.getElementById('phones-container');
    const inputNumber = document.getElementById('phone-number');
    const selectType = document.getElementById('phone-type');

    if (btnAdd) {
        btnAdd.addEventListener('click', (e) => {
            e.preventDefault(); // Detiene el "?" en la URL

            const num = inputNumber.value.trim();
            const type = selectType.value;

            if (num === "") return alert("Introduce un número válido");

            // Crear la "cajita" visual
            const card = document.createElement('div');
            card.className = 'phone-card';
            card.innerHTML = `
                <div class="phone-info">
                    <b>[${type}]</b> <span>${num}</span>
                </div>
                <button type="button" class="btn-remove">DESVINCULAR</button>
                <input type="hidden" name="telefonos[]" value="${type}:${num}">
            `;

            container.appendChild(card);

            // Limpiar para el siguiente
            inputNumber.value = "";
            
            // Lógica para borrar la cajita
            card.querySelector('.btn-remove').addEventListener('click', () => {
                card.remove();
            });
        });
    }
});