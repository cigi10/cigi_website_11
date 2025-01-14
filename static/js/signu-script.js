async function generateSignal() {
    const equation = document.getElementById('equation').value;
    if (!equation.trim()) {
        alert("Please enter a valid equation.");
        return;
    }
    try {
        const response = await fetch('/plot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ equation }),
        });
        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.error}`);
            return;
        }
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);
        const img = document.getElementById('signal-plot');
        img.src = imageUrl;
    } catch (err) {
        console.error(err);
        alert("An error occurred while generating the signal.");
    }
}
