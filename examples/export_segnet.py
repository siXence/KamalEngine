dependencies = ['torch', 'kamal']

from kamal.vision.models.segmentation import segnet_vgg16_bn

if __name__=='__main__':
    import kamal, torch
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', choices=['seg', 'depth'])
    parser.add_argument('--ckpt')
    args = parser.parse_args()

    num_classes = {
        'seg': 13,
        'depth': 1,
    }[args.task]

    visual_task = {
        'seg': kamal.hub.meta.TASK.SEGMENTATION,
        'depth': kamal.hub.meta.TASK.DEPTH
    }[args.task]
    
    model = segnet_vgg16_bn(pretrained=False, num_classes=num_classes)
    model.load_state_dict( torch.load(args.ckpt) )
    kamal.hub.save(
        model,
        save_path='exported/segnet_vgg16_bn_nyuv2_%s'%args.task,
        entry_name='segnet_vgg16_bn',
        spec_name=None,
        code_path=__file__,
        metadata=kamal.hub.meta.Metadata(
            name='segnet_vgg16_bn_nyuv2_%s'%(args.task),
            dataset='nyuv2',
            task=visual_task,
            url='https://github.com/zju-vipa/KamalEngine',
            input=kamal.hub.meta.ImageInput(
                size=240,
                range=[0, 1],
                space='rgb',
                normalize=dict(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ),
            entry_args=dict(num_classes=num_classes),
            other_metadata=dict(num_classes=num_classes),
        )
    )
