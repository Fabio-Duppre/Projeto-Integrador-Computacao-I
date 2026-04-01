        // Itens do Questionário
        const questions = [
            { id: 1, type: 'stress', text: "Achei difícil me acalmar." },
            { id: 2, type: 'anxiety', text: "Senti minha boca seca." },
            { id: 3, type: 'depression', text: "Não consegui sentir nenhum sentimento positivo." },
            { id: 4, type: 'anxiety', text: "Tive dificuldade em respirar (ex. respiração excessivamente rápida, falta de ar sem esforço físico)." },
            { id: 5, type: 'depression', text: "Achei difícil ter iniciativa para fazer as coisas." },
            { id: 6, type: 'stress', text: "Tive a tendência a reagir de forma exagerada às situações." },
            { id: 7, type: 'anxiety', text: "Senti tremores (ex. nas mãos)." },
            { id: 8, type: 'stress', text: "Senti que estava sempre nervoso(a)." },
            { id: 9, type: 'anxiety', text: "Preocupei-me com situações em que eu pudesse entrar em pânico e parecer ridículo(a)." },
            { id: 10, type: 'depression', text: "Senti que não tinha nada a desejar para o futuro." },
            { id: 11, type: 'stress', text: "Senti-me agitado(a)." },
            { id: 12, type: 'stress', text: "Achei difícil relaxar." },
            { id: 13, type: 'depression', text: "Senti-me triste e deprimido(a)." },
            { id: 14, type: 'stress', text: "Fui intolerante com qualquer coisa que me impedisse de continuar o que eu estava fazendo." },
            { id: 15, type: 'anxiety', text: "Senti que estava prestes a entrar em pânico." },
            { id: 16, type: 'depression', text: "Fui incapaz de me entusiasmar com qualquer coisa." },
            { id: 17, type: 'depression', text: "Senti que não tinha muito valor como pessoa." },
            { id: 18, type: 'stress', text: "Senti que estava um pouco sensível demais." },
            { id: 19, type: 'anxiety', text: "Senti os batimentos do meu coração alterados mesmo sem ter feito esforço físico." },
            { id: 20, type: 'anxiety', text: "Senti medo sem motivo aparente." },
            { id: 21, type: 'depression', text: "Senti que a vida não tinha sentido." }
        ];

        let currentStep = 0;
        let answers = new Array(questions.length).fill(null);
        
        function startSurvey() {
            document.getElementById('intro-section').classList.add('hidden');
            document.getElementById('form-section').classList.remove('hidden');
            renderQuestion();
        }

        function renderQuestion() {
            const q = questions[currentStep];
            const container = document.getElementById('question-container');
            
            container.innerHTML = `
                <div class="animate-fade">
                    <span class="inline-block px-3 py-1 bg-blue-100 text-blue-600 rounded-lg text-xs font-bold mb-4 uppercase tracking-widest">Questão ${currentStep + 1}</span>
                    <h2 class="text-xl md:text-2xl font-semibold text-gray-800 mb-8 leading-tight">${q.text}</h2>
                    <div class="grid grid-cols-1 gap-4">
                        ${[0, 1, 2, 3].map(value => {
                            const labels = [
                                "Não se aplicou de maneira alguma",
                                "Aplicou-se em algum grau ou por pouco tempo",
                                "Aplicou-se em um grau considerável",
                                "Aplicou-se muito ou na maioria do tempo"
                            ];
                            const isSelected = answers[currentStep] === value;
                            return `
                                <div onclick="selectOption(${value})" class="option-card cursor-pointer p-5 border-2 rounded-2xl transition-all flex items-center ${isSelected ? 'option-selected' : 'border-gray-100'}">
                                    <div class="w-10 h-10 rounded-xl border-2 flex items-center justify-center mr-5 transition-colors ${isSelected ? 'bg-blue-600 border-blue-600 text-white' : 'border-gray-200 text-gray-400'}">
                                        <span class="font-bold">${value}</span>
                                    </div>
                                    <span class="text-gray-700 font-medium md:text-lg">${labels[value]}</span>
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>
            `;

            updateUI();
        }

        function selectOption(val) {
            answers[currentStep] = val;
            renderQuestion();
            /* To do - Validar a necessidade disso aqui */
            setTimeout(() => {
                if (currentStep < questions.length - 1) {
                    nextQuestion();
                } else {
                    document.getElementById('next-btn').disabled = false;
                }
            }, 350);
        }

        function nextQuestion() {
            if (currentStep < questions.length -1) {
                currentStep++;
                renderQuestion();
            } else {
                showResults();
            }
        }

        function prevQuestion() {
            if (currentStep > 0) {
                currentStep--;
                renderQuestion();
            }
        }

        function updateUI() {
            const progress = ((currentStep + 1) / questions.length) * 100;
            document.getElementById('progress-bar').style.width = `${progress}%`;
            document.getElementById('progress-text').innerText = `Questão ${currentStep + 1} de 21`;
            document.getElementById('progress-percent').innerText = `${Math.round(progress)}%`;

            document.getElementById('prev-btn').style.visibility = currentStep === 0 ? 'hidden' : 'visible';
            document.getElementById('next-btn').disabled = answers[currentStep] === null;
            document.getElementById('next-btn').innerHTML = currentStep === questions.length - 1 ? 'Finalizar <i class="fas fa-check ml-2"></i>' : 'Próxima <i class="fas fa-chevron-right ml-2"></i>';
        }

        function showResults() {
            let dScore = 0, aScore = 0, sScore = 0;

            questions.forEach((q, i) => {
                if (q.type === 'depression') dScore += answers[i];
                if (q.type === 'anxiety') aScore += answers[i];
                if (q.type === 'stress') sScore += answers[i];
            });

            updateScoreDisplay('depression', dScore * 2);
            updateScoreDisplay('anxiety', aScore * 2);
            updateScoreDisplay('stress', sScore * 2);

            document.getElementById('form-section').classList.add('hidden');
            document.getElementById('results-section').classList.remove('hidden');
            console.log("to aqui", dScore*2, aScore*2, sScore*2)
            /*To do - mandar os valores pro banco daqui */
            //dScore - aScore - sScore

            // valores que serão enviados ao banco        
            let data_resposta = new Date().toISOString().split("T")[0];
            let name = document.getElementById("name").textContent
            let age = parseInt(document.getElementById("age").textContent, 10)
            let course = document.getElementById("course").textContent

            dScore = dScore * 2
            aScore = aScore * 2
            sScore = sScore * 2

            console.log("Entrando no fetch")                        
            fetch("/registrar", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body:`name=${encodeURIComponent(name)}&age=${encodeURIComponent(age)}&course=${encodeURIComponent(course)}&data_resposta=${encodeURIComponent(data_resposta)}&dScore=${encodeURIComponent(dScore)}&aScore=${encodeURIComponent(aScore)}&sScore=${encodeURIComponent(sScore)}`
            })
        }

        function updateScoreDisplay(type, finalScore) {
            const el = document.getElementById(`score-${type}`);
            const label = document.getElementById(`label-${type}`);
            el.innerText = finalScore;

            const cuts = {
                depression: [10, 14, 21, 28],
                anxiety: [8, 10, 15, 20],
                stress: [15, 19, 26, 34]
            };

            const t = cuts[type];
            let status = "Normal", color = "bg-green-100 text-green-700";

            if (finalScore >= t[3]) { status = "Extremamente Severo"; color = "bg-red-100 text-red-700"; }
            else if (finalScore >= t[2]) { status = "Severo"; color = "bg-orange-100 text-orange-700"; }
            else if (finalScore >= t[1]) { status = "Moderado"; color = "bg-yellow-100 text-yellow-700"; }
            else if (finalScore >= t[0]) { status = "Leve"; color = "bg-blue-100 text-blue-700"; }

            label.innerText = status;
            label.className = `inline-block px-4 py-1 rounded-full text-xs font-bold uppercase ${color}`;                        
        }

        function voltarHomepage(){
            window.location.href = "/";
        }
      
        console.log(document.getElementById('name').textContent)
        console.log(document.getElementById('age').textContent)
        console.log(document.getElementById('course').textContent)