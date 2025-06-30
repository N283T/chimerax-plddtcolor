# vim: set expandtab shiftwidth=4 softtabstop=4:

from chimerax.core.commands import CmdDesc, EmptyArg, Or
from chimerax.atomic import AtomsArg, Atoms
import numpy as np


class PLDDTColorer:
    """Class for coloring atoms based on pLDDT values"""

    def __init__(self, session):
        self.session = session
        # Default color scheme (threshold, RGBA values)
        self.color_map = [
            (100, (0, 83, 214, 255)),    # #0053D6
            (90, (101, 203, 243, 255)),  # #65CBE3
            (70, (255, 219, 19, 255)),   # #FFDB13
            (50, (255, 125, 69, 255)),   # #FF7D45
        ]

    def color_atoms(self, atoms=None):
        """Main method to color atoms based on pLDDT values"""
        if atoms is None:
            models = self._get_all_models()
        else:
            models = self._group_atoms_by_model(atoms)

        if not models:
            self.session.logger.warning("No models found")
            return

        # Collect and process statistics for all models
        all_stats = self._process_all_models(models)
        if all_stats:
            self._display_combined_stats(all_stats)

    def _get_all_models(self):
        """Get all models from the session"""
        from chimerax.core.commands import all_objects
        models = all_objects(self.session).models
        return [(model, model.atoms) for model in models
                if hasattr(model, 'atoms') and len(model.atoms) > 0]

    def _group_atoms_by_model(self, atoms):
        """Group atoms by model"""
        models_dict = {}
        for atom in atoms:
            model = atom.structure
            if model not in models_dict:
                models_dict[model] = []
            models_dict[model].append(atom)

        return [(model, Atoms(model_atoms_list))
                for model, model_atoms_list in models_dict.items()
                if len(model_atoms_list) > 0]

    def _model_id_to_str(self, model_id):
        """Convert model ID to string"""
        if isinstance(model_id, tuple):
            return ".".join(str(x) for x in model_id)
        else:
            return str(model_id)

    def _process_all_models(self, models):
        """Process all models and collect statistics"""
        all_stats = []
        for model, atoms in models:
            model_id = self._model_id_to_str(model.id)
            self.session.logger.info(
                f"Processing model: #{model_id} {model.name}")
            stats = self._process_model_atoms(atoms)
            if stats:
                all_stats.append((model.name, model_id, stats))
        return all_stats

    def _process_model_atoms(self, atoms):
        """Process a specific set of atoms"""
        if len(atoms) == 0:
            return None

        # Get pLDDT values
        try:
            bfactors = atoms.bfactors
        except Exception as e:
            self.session.logger.error(f"Error getting pLDDT values: {e}")
            return None

        # Apply color scheme
        self._apply_color_scheme(atoms, bfactors)

        # Update ribbon colors
        self._update_ribbon_colors(atoms)

        self.session.logger.info("pLDDT-based coloring completed\n")

        # Return statistics
        return self._calculate_statistics(bfactors)

    def _apply_color_scheme(self, atoms, bfactors):
        """Apply color scheme based on pLDDT values"""
        for cutoff, color in self.color_map:
            mask = bfactors < cutoff
            if mask.any():
                atoms.filter(mask).colors = color
                self.session.logger.info(
                    f"Colored {mask.sum()} atoms with pLDDT < {cutoff}")

    def _update_ribbon_colors(self, atoms):
        """Update ribbon display colors"""
        try:
            residues = atoms.unique_residues
            for residue in residues:
                residue_atoms = residue.atoms
                if len(residue_atoms) > 0:
                    avg_color = residue_atoms.colors.mean(axis=0).astype(int)
                    residue.ribbon_color = tuple(avg_color)
        except Exception as e:
            self.session.logger.warning(f"Could not update ribbon colors: {e}")

    def _calculate_statistics(self, bfactors):
        """Calculate statistics from bfactor values"""
        return {
            'min': min(bfactors),
            'max': max(bfactors),
            'mean': np.mean(bfactors),
            'median': np.median(bfactors),
            'std': np.std(bfactors),
            'total': len(bfactors)
        }

    def _display_combined_stats(self, all_stats):
        """Display combined statistics for multiple models"""
        if not all_stats:
            return

        # Collect statistics data
        model_names = [name for name, _, _ in all_stats]
        model_ids = [model_id for _, model_id, _ in all_stats]
        stats_data = {
            'min': [stats['min'] for _, _, stats in all_stats],
            'max': [stats['max'] for _, _, stats in all_stats],
            'mean': [stats['mean'] for _, _, stats in all_stats],
            'median': [stats['median'] for _, _, stats in all_stats],
            'std': [stats['std'] for _, _, stats in all_stats],
            'total': [stats['total'] for _, _, stats in all_stats]
        }

        # Create HTML table
        html_table = self._create_stats_table(
            model_names, model_ids, stats_data)

        # Display in log
        self.session.logger.info("Combined statistics for all models:")
        self.session.logger.info(html_table, is_html=True)

    def _create_stats_table(self, model_names, model_ids, stats_data):
        """Create HTML table for statistics"""
        html_table = """
        <table style="border-collapse: collapse; border: 1px solid #ccc; margin: 10px 0;">
            <tr style="background-color: #f0f0f0;">
                <th style="border: 1px solid #ccc; padding: 8px; text-align: left;">Model</th>
                <th style="border: 1px solid #ccc; padding: 8px; text-align: center;">ID</th>
                <th style="border: 1px solid #ccc; padding: 8px; text-align: right;">Min</th>
                <th style="border: 1px solid #ccc; padding: 8px; text-align: right;">Max</th>
                <th style="border: 1px solid #ccc; padding: 8px; text-align: right;">Mean</th>
                <th style="border: 1px solid #ccc; padding: 8px; text-align: right;">Median</th>
                <th style="border: 1px solid #ccc; padding: 8px; text-align: right;">Std Dev</th>
                <th style="border: 1px solid #ccc; padding: 8px; text-align: right;">Total Atoms</th>
            </tr>
        """

        for i, (model_name, model_id) in enumerate(zip(model_names, model_ids)):
            bg_color = "#f9f9f9" if i % 2 == 1 else ""

            html_table += f"""
            <tr style="background-color: {bg_color};">
                <td style="border: 1px solid #ccc; padding: 8px;">{model_name}</td>
                <td style="border: 1px solid #ccc; padding: 8px; text-align: center;">{model_id}</td>
                <td style="border: 1px solid #ccc; padding: 8px; text-align: right;">{stats_data['min'][i]:.2f}</td>
                <td style="border: 1px solid #ccc; padding: 8px; text-align: right;">{stats_data['max'][i]:.2f}</td>
                <td style="border: 1px solid #ccc; padding: 8px; text-align: right;">{stats_data['mean'][i]:.2f}</td>
                <td style="border: 1px solid #ccc; padding: 8px; text-align: right;">{stats_data['median'][i]:.2f}</td>
                <td style="border: 1px solid #ccc; padding: 8px; text-align: right;">{stats_data['std'][i]:.2f}</td>
                <td style="border: 1px solid #ccc; padding: 8px; text-align: right;">{stats_data['total'][i]}</td>
            </tr>
            """

        html_table += "</table>"
        return html_table


def color_plddt(session, atoms=None):
    """Color atoms based on pLDDT values - command interface"""
    colorer = PLDDTColorer(session)
    colorer.color_atoms(atoms)


color_plddt_desc = CmdDesc(
    required=[("atoms", Or(AtomsArg, EmptyArg))],
)
