using UnityEngine;

public abstract class VisualState
{
    protected VisualController controller;

    protected VisualState(VisualController controller)
    {
        this.controller = controller;
    }

    public abstract void Enter();
    public abstract void Update();
    public abstract void Exit();
}
