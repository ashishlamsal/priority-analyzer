# Proirity Analyzer

This repository is a backend for **BE Admission Rank and Priority Analyzer** project. This project was done as an academic project assigned by the Department of Electronics and Computer Engineering, Pulchowk Campus under the subject Database Management System and Software Engineering.

![Python][Python]&nbsp;
![Django][Django]&nbsp;
![React][React]&nbsp;
![HTML][HTML]&nbsp;
![CSS][CSS]&nbsp;
![Git][Git]&nbsp;
![Visual Studio Code][Visual Studio Code]&nbsp;

## Links

> - Frontend : <https://github.com/Atomnp/priority-analyser-frontend>
> - Backend : <https://github.com/ashishlamsal/priority-analyzer>

## Database Visualization

![ModelGraph][ModelGraph]&nbsp;

## App Visualization

![RankGraph][RankGraph]&nbsp;

## Usage

```powershell
    git clone https://github.com/ashishlamsal/priority-analyzer.git
    cd priority-analyzer/
    python -m venv venv
    ./venv/Scripts/activate
    pip install -r requirements.txt
    cd admission/
    python manage.py runserver
```

## API Documentation

Detailed documentation of API can be found at `/docs`

## Generate graphs for models

```powershell
    python ./manage.py graph_models rank --arrow-shape normal > ./dotfiles/rank_models.dot
    python ./manage.py graph_models -a --arrow-shape normal > ./dotfiles/project.dot
    python ./manage.py graph_models --pydot rank --arrow-shape normal -g -o rank_models_visualized.svg
    python ./manage.py graph_models --pydot -a --arrow-shape normal -g -o rank_app_visualized.svg
```

[Python]: https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=ffffff
[Django]: https://img.shields.io/badge/-Django-092E20?style=flat-square&logo=django&logoColor=ffffff
[React]: https://img.shields.io/badge/-React-61DAFB?style=flat-square&logo=react&logoColor=12232E
[HTML]: https://img.shields.io/badge/-HTML-E34F26?style=flat-square&logo=HTML5&logoColor=ffffff
[CSS]: https://img.shields.io/badge/-CSS-1572B6?style=flat-square&logo=CSS3&logoColor=1572B6&logoColor=ffffff
[Git]: https://img.shields.io/badge/-Git-F05032?style=flat-square&logo=git&logoColor=ffffff
[Visual Studio Code]: https://img.shields.io/badge/-Visual%20Studio%20Code-007ACC?style=flat-square&logo=visual-studio-code&logoColor=ffffff
[ModelGraph]: ./admission/graphs/rank_models_visualized_1.svg "Rank Models"
[RankGraph]: ./admission/graphs/rank_app_visualized_1.svg "Rank App"
