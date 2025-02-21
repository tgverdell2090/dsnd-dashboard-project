from fasthtml.common import *
import matplotlib.pyplot as plt

# Import QueryBase, Employee, Team from employee_events
from employee_events import QueryBase, Employee, Team

# import the load_model function from the utils.py file
from utils import load_model

from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
)

from combined_components import FormGroup, CombinedComponent

app, route = fast_app()

class ReportDropdown(Dropdown):
    def build_component(self, asset_id, model):
        self.label = model.name if model else ""
        return super().build_component(asset_id, model)
    
    def component_data(self, asset_id, model):
        if model is None:
            return [("Select...", "1")]
        try:
            data = model.names()
            if not data:
                return [("No options available", "1")]
            return data
        except Exception as e:
            print(f"Error getting dropdown data: {e}")
            return [("Error loading options", "1")]

class Header(BaseComponent):
    def build_component(self, asset_id, model):
        title = "Team Performance" if model.name == "team" else "Employee Performance"
        return H1(title)

class LineChart(MatplotlibViz):
    def visualization(self, asset_id, model):
        data = model.event_counts(asset_id)
        
        if data.empty:
            fig, ax = plt.subplots()
            ax.set_title('No Data Available')
            self.set_axis_styling(ax)
            return fig
        
        data = data.fillna(0)
        data = data.set_index('event_date')
        data = data.sort_index()
        data = data.cumsum()
        
        data.columns = ['Positive', 'Negative']
        
        fig, ax = plt.subplots()
        data.plot(ax=ax)
        
        self.set_axis_styling(ax)
        ax.set_title('Cumulative Events Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Events')
        
        return fig

class BarChart(MatplotlibViz):
    predictor = load_model()

    def visualization(self, asset_id, model):
        data = model.model_data(asset_id)
        probs = self.predictor.predict_proba(data)
        probs = probs[:, 1]
        
        pred = probs.mean() if model.name == "team" else probs[0]
        
        fig, ax = plt.subplots()
        
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        
        self.set_axis_styling(ax)
        
        return fig

class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls='grid')

class NotesTable(DataTable):
    def component_data(self, entity_id, model):
        return model.notes(entity_id)

class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method = "POST"
    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
        ),
        ReportDropdown(
            id="selector",
            name="user-selection")
    ]

class Report(CombinedComponent):
    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable()
    ]

# Initialize Report
report = Report()

@app.route('/')
def home():
    return report(1, Employee())

@app.route('/employee/{id}')
def employee_profile(id: str):
    return report(id, Employee())

@app.route('/team/{id}')
def team_profile(id: str):
    return report(id, Team())

@app.route('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    profile_type = r.query_params.get('profile_type')
    if profile_type == 'Team':
        return dropdown(None, Team())
    elif profile_type == 'Employee':
        return dropdown(None, Employee())

@app.route('/update_data')
async def update_data(r):
    form = await r.form()
    profile_type = form._dict['profile_type']
    id = form._dict['user-selection']
    
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)

serve()